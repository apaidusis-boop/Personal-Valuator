"""Security audit perpetuum — port of OpenClaw skills/healthcheck/SKILL.md.

Read-only checks (NEVER modifies state). Surfaces findings via score+flags
and writes a digest to obsidian_vault/workspace/SECURITY_AUDIT.md.

Subjects (one each):
  - env_secrets       — .env not in git history; permissions; required keys present
  - git_secrets       — no committed credentials/tokens in HEAD or recent history
  - dependencies      — pip outdated + known CVE scan (pip-audit if installed)
  - file_permissions  — sensitive files (.env, *.db) not world-writable
  - telegram_token    — token rotation freshness (last rotation date)

Each subject scored 0-100. Flags surfaced. Critical findings (score < 30)
trigger Telegram push if NOTIFY_ON_AUDIT enabled in config.

NEVER auto-fixes. NEVER deletes. NEVER pushes to remote. T1 Observer only.
"""
from __future__ import annotations

import os
import re
import shutil
import stat
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

from ._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"
GITIGNORE_PATH = ROOT / ".gitignore"
DIGEST_PATH = ROOT / "obsidian_vault" / "workspace" / "SECURITY_AUDIT.md"

# Known credential patterns (very narrow; false-positive averse)
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),                           # AWS access key
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),                        # OpenAI / Anthropic tokens
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),                       # GitHub PAT
    re.compile(r"(?i)bot[0-9]+:[A-Za-z0-9_-]{30,}"),           # Telegram bot token shape
]


class SecurityAuditPerpetuum(BasePerpetuum):
    """Read-only host hardening + secret hygiene scan."""

    name = "security_audit"
    description = "Host security: .env hygiene, git secrets, dep CVEs, file perms, token rotation"
    autonomy_tier = "T1"
    enabled = True
    drop_alert_threshold = 20

    def subjects(self) -> list[PerpetuumSubject]:
        return [
            PerpetuumSubject(id="env_secrets", label=".env file hygiene"),
            PerpetuumSubject(id="git_secrets", label="git history credential scan"),
            PerpetuumSubject(id="dependencies", label="dependency CVE scan"),
            PerpetuumSubject(id="file_permissions", label="sensitive file permissions"),
            PerpetuumSubject(id="telegram_token", label="Telegram token rotation freshness"),
        ]

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        try:
            return getattr(self, f"_score_{subject.id}")(subject)
        except AttributeError:
            return PerpetuumResult(
                subject_id=subject.id, score=-1,
                flags=["unimplemented_check"],
            )

    # ─── Individual checks ───────────────────────────────────────────────

    def _score_env_secrets(self, s: PerpetuumSubject) -> PerpetuumResult:
        flags: list[str] = []
        details: dict = {}
        score = 100

        if not ENV_PATH.exists():
            flags.append("env_missing")
            score = 50
            details["env_exists"] = False
            return PerpetuumResult(subject_id=s.id, score=score,
                                   flag_count=len(flags), flags=flags, details=details)

        details["env_exists"] = True
        # Is .env in .gitignore?
        ignored = False
        if GITIGNORE_PATH.exists():
            ignored = ".env" in GITIGNORE_PATH.read_text(encoding="utf-8", errors="ignore")
        details["env_in_gitignore"] = ignored
        if not ignored:
            flags.append("env_not_gitignored")
            score -= 50

        # File permissions check (POSIX-ish; on Windows os.stat returns mode bits but world-writable rare)
        try:
            mode = ENV_PATH.stat().st_mode
            world_readable = bool(mode & stat.S_IROTH)
            details["env_world_readable"] = world_readable
            if world_readable and os.name != "nt":
                flags.append("env_world_readable")
                score -= 20
        except Exception:
            pass

        # Required keys present?
        required = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
        try:
            content = ENV_PATH.read_text(encoding="utf-8", errors="ignore")
            missing = [k for k in required if f"{k}=" not in content]
            details["missing_keys"] = missing
            if missing:
                flags.append(f"missing_keys:{len(missing)}")
                score -= 10 * len(missing)
        except Exception as e:
            flags.append(f"env_read_error:{e}")
            score -= 30

        action_hint = None
        if "env_not_gitignored" in flags:
            action_hint = "Adicionar .env ao .gitignore IMEDIATAMENTE; rotacionar todos os tokens depois."
        return PerpetuumResult(
            subject_id=s.id, score=max(0, score),
            flag_count=len(flags), flags=flags, details=details,
            action_hint=action_hint,
        )

    def _score_git_secrets(self, s: PerpetuumSubject) -> PerpetuumResult:
        """Scan recent git diffs (last 50 commits) for credential patterns."""
        flags: list[str] = []
        details: dict = {}
        score = 100

        if not shutil.which("git"):
            return PerpetuumResult(subject_id=s.id, score=-1,
                                   flags=["git_not_installed"])

        try:
            r = subprocess.run(
                ["git", "log", "-50", "-p", "--", ":!*.lock", ":!*.json", ":!*.svg"],
                capture_output=True, text=True, timeout=60, cwd=str(ROOT),
                encoding="utf-8", errors="replace",
            )
            diff = r.stdout or ""
            details["scanned_chars"] = len(diff)
        except Exception as e:
            return PerpetuumResult(subject_id=s.id, score=-1,
                                   flags=[f"git_log_failed:{type(e).__name__}"])

        hits: list[str] = []
        for pat in SECRET_PATTERNS:
            for m in pat.finditer(diff):
                snippet = m.group(0)
                # Truncate before reporting (don't expose full secret)
                hits.append(snippet[:8] + "..." + snippet[-4:] if len(snippet) > 16 else snippet[:6] + "...")
                if len(hits) >= 5:
                    break
            if len(hits) >= 5:
                break
        details["hits"] = hits
        if hits:
            flags.append(f"secret_pattern_in_history:{len(hits)}")
            score -= min(80, len(hits) * 30)

        action_hint = None
        if hits:
            action_hint = ("Rotacionar credentials expostas + considerar rewrite history "
                           "(git filter-repo). Rotação primeiro, history depois.")
        return PerpetuumResult(
            subject_id=s.id, score=max(0, score),
            flag_count=len(flags), flags=flags, details=details,
            action_hint=action_hint,
        )

    def _score_dependencies(self, s: PerpetuumSubject) -> PerpetuumResult:
        flags: list[str] = []
        details: dict = {}
        score = 100

        # Try pip-audit (preferred; CVE-aware)
        if shutil.which("pip-audit"):
            try:
                r = subprocess.run(
                    ["pip-audit", "--format", "json", "--progress-spinner", "off"],
                    capture_output=True, text=True, timeout=180,
                )
                import json as _json
                data = _json.loads(r.stdout) if r.stdout else {}
                vulns = data.get("dependencies", []) if isinstance(data, dict) else []
                vuln_count = sum(1 for d in vulns if d.get("vulns"))
                details["tool"] = "pip-audit"
                details["vulnerable_packages"] = vuln_count
                if vuln_count > 0:
                    flags.append(f"cve_count:{vuln_count}")
                    score -= min(70, vuln_count * 10)
            except Exception as e:
                flags.append(f"pip_audit_error:{type(e).__name__}")
                score = 50  # unknown state
        else:
            details["tool"] = "none"
            flags.append("pip_audit_not_installed")
            score = 70  # not blocking, but degraded confidence

        action_hint = None
        if "cve_count:" in str(flags):
            action_hint = "pip-audit --fix (review changes) ou pip install -U <pkg> manualmente para CVEs críticas."
        elif "pip_audit_not_installed" in flags:
            action_hint = "pip install pip-audit  # para scans periódicos de CVEs."
        return PerpetuumResult(
            subject_id=s.id, score=max(0, score),
            flag_count=len(flags), flags=flags, details=details,
            action_hint=action_hint,
        )

    def _score_file_permissions(self, s: PerpetuumSubject) -> PerpetuumResult:
        """Walk sensitive paths; flag world-writable on POSIX."""
        flags: list[str] = []
        details: dict = {}
        score = 100

        if os.name == "nt":
            details["skipped"] = "windows: posix permission model not enforced"
            return PerpetuumResult(subject_id=s.id, score=90,
                                   flag_count=0, flags=[], details=details)

        sensitive = [ROOT / ".env", ROOT / "data"]
        bad: list[str] = []
        for p in sensitive:
            if not p.exists():
                continue
            try:
                mode = p.stat().st_mode
                if mode & stat.S_IWOTH:
                    bad.append(str(p.relative_to(ROOT)))
            except Exception:
                continue
        details["world_writable"] = bad
        if bad:
            flags.append(f"world_writable:{len(bad)}")
            score -= min(60, len(bad) * 25)

        action_hint = None
        if bad:
            action_hint = f"chmod 600 {' '.join(bad)}  # remover write para others"
        return PerpetuumResult(
            subject_id=s.id, score=max(0, score),
            flag_count=len(flags), flags=flags, details=details,
            action_hint=action_hint,
        )

    def _score_telegram_token(self, s: PerpetuumSubject) -> PerpetuumResult:
        """Check token rotation freshness — assumes user tracks via TELEGRAM_TOKEN_ROTATED in .env."""
        flags: list[str] = []
        details: dict = {}
        score = 100

        if not ENV_PATH.exists():
            return PerpetuumResult(subject_id=s.id, score=-1, flags=["env_missing"])

        content = ENV_PATH.read_text(encoding="utf-8", errors="ignore")
        if "TELEGRAM_BOT_TOKEN=" not in content:
            return PerpetuumResult(subject_id=s.id, score=-1,
                                   flags=["no_telegram_configured"])

        m = re.search(r"TELEGRAM_TOKEN_ROTATED=([0-9-]+)", content)
        if not m:
            flags.append("rotation_date_missing")
            score = 60
            details["last_rotated"] = None
        else:
            try:
                last = date.fromisoformat(m.group(1))
                age_days = (date.today() - last).days
                details["last_rotated"] = last.isoformat()
                details["age_days"] = age_days
                if age_days > 365:
                    flags.append(f"stale_token:{age_days}d")
                    score -= 30
                elif age_days > 180:
                    flags.append(f"aging_token:{age_days}d")
                    score -= 10
            except ValueError:
                flags.append("rotation_date_unparseable")
                score = 50

        action_hint = None
        if score < 80:
            action_hint = ("Considerar rotacionar TELEGRAM_BOT_TOKEN via @BotFather → "
                           "/revoke ou /token; actualizar TELEGRAM_TOKEN_ROTATED=YYYY-MM-DD em .env.")
        return PerpetuumResult(
            subject_id=s.id, score=max(0, score),
            flag_count=len(flags), flags=flags, details=details,
            action_hint=action_hint,
        )

    # ─── Override run() to write digest after standard scoring ───────────

    def run(self, run_date: str | None = None, dry_run: bool = False) -> dict:
        result = super().run(run_date=run_date, dry_run=dry_run)
        if not dry_run:
            try:
                self._write_digest(result, run_date or date.today().isoformat())
            except Exception as e:
                result["errors"].append(f"digest: {type(e).__name__}: {e}")
        return result

    def _write_digest(self, run_summary: dict, run_date: str) -> None:
        """Overwrite SECURITY_AUDIT.md with current snapshot."""
        DIGEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "---",
            "title: SECURITY_AUDIT",
            f"last_run: {run_date}",
            "purpose: Read-only security audit. Generated by security_audit perpetuum.",
            "edit: read-only generated; nunca commit credentials sem rotacionar.",
            "---",
            "",
            f"# 🛡️ Security Audit — {run_date}",
            "",
            f"_Subjects scanned: {run_summary['scored']}/{run_summary['subjects']}, "
            f"{run_summary['alerts']} alerts, {len(run_summary['errors'])} errors._",
            "",
            "## Findings",
            "",
        ]
        for r in run_summary["results"]:
            score = r["score"]
            icon = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"
            if score < 0:
                icon = "⚪"
            lines.append(f"### {icon} `{r['subject']}` — score {score}")
            if r["action_hint"]:
                lines.append(f"**Action**: {r['action_hint']}")
            lines.append("")
        if run_summary["errors"]:
            lines.append("## Errors")
            for e in run_summary["errors"]:
                lines.append(f"- ❌ {e}")
            lines.append("")
        DIGEST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
