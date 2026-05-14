"""Code Health Perpetuum — apanha anti-patterns recorrentes no codebase.

USER REQUEST (2026-04-26): "isso o TI já deveria estar fazendo sozinho.
Localizando os bugs e fixing eles." Este perpetuum é a infra que o utilizador
pediu — em vez de descobrir bugs por acidente, varre o repo todos os dias.

Subjects: cada `.py` em SCAN_DIRS.

Anti-patterns detectados (deduct pontos por sinal):
  CH001 — yaml.safe_load(catalog.yaml) directo, em vez de library.ri.catalog
          (causa o "watchlist not in catalog loop" recorrente)
  CH002 — itera só `cat.get("stocks")` quando catalog tem watchlist_stocks
  CH003 — itera só `cat.get("fiis")` quando catalog tem watchlist_fiis
  CH004 — constante `CATALOG = .../catalog.yaml` definida mas nunca usada
          (cruft após refactor incompleto)
  CH005 — hard-coded "http://localhost:11434/api/generate" + requests.post
          (deve usar agents._llm.ollama_call; canonical 2026-04-27)
  CH006 — `except:` ou `except Exception:` sem log/raise (silent error swallow)
  CH007 — section banner ad-hoc (`print(f"\\n{'=' * 60}\\n== ...")`); usar
          agents._common.section
  CH008 — Python file length warning: file > 500 source lines (excl. blank +
          pure-comment lines). Soft signal; no auto-fix. Anthropic best practice.

Score 0-100. <70 → action_hint com refactor concreto.

T1 Observer por defeito. Promote para T2 quando estável (auto-propor PR-style action).

Adicionar nova regra: criar nova função `_check_chXXX` e juntar à lista CHECKS.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

SCAN_DIRS = ["agents", "fetchers", "scripts", "scoring", "analytics", "library"]
ALLOWLIST_PATHS = {
    # Estes ficheiros têm permissão para fazer yaml.safe_load directo:
    "library/ri/catalog.py",                  # o próprio accessor
    "library/ri/catalog_autopopulate.py",     # writer, não reader
    "agents/perpetuum/code_health.py",        # este ficheiro analisa o padrão
}

# CH005/006/007 allowlists (the canonical home + this scanner)
ALLOWLIST_OLLAMA_DIRECT = {
    "agents/_llm.py",                         # canonical wrapper
    "agents/perpetuum/code_health.py",        # scanner
    "fetchers/news_fetch.py",                 # uses /api/chat (different endpoint)
    "scripts/vault_ask.py",                   # uses /api/chat + /api/embed
    "library/rag.py",                         # uses /api/embed primarily
    # overnight one-shots are off-limits (scripts/overnight/*.py)
}
ALLOWLIST_BARE_EXCEPT = {
    "agents/perpetuum/code_health.py",
}
ALLOWLIST_AD_HOC_BANNER = {
    "agents/_common.py",                      # canonical home
    "agents/perpetuum/code_health.py",        # scanner
}

# --- regex pre-compiled ---

# yaml.safe_load(<...>catalog.yaml...) ou yaml.safe_load(CATALOG.read_text(...))
RE_DIRECT_LOAD_CATALOG = re.compile(
    r'yaml\.safe_load\(\s*[A-Za-z_][\w\.]*'
    r'(?:\.read_text\([^)]*\))?\s*\)',
    re.M,
)
RE_CATALOG_PATH_CONST = re.compile(
    r'^\s*([A-Z_][A-Z0-9_]*)\s*=\s*[^\n]*catalog\.yaml',
    re.M,
)
RE_STOCKS_ONLY = re.compile(r'\.get\(\s*["\']stocks["\']\s*(?:,\s*\[\s*\])?\s*\)')
RE_FIIS_ONLY = re.compile(r'\.get\(\s*["\']fiis["\']\s*(?:,\s*\[\s*\])?\s*\)')
RE_HAS_WATCHLIST = re.compile(r'watchlist_(?:stocks|fiis)')

# --- check functions ---

def _check_ch001_direct_catalog_load(src: str, rel: str) -> tuple[int, str | None]:
    """Direct yaml.safe_load on catalog.yaml file path."""
    if "catalog.yaml" not in src:
        return 0, None
    has_load = "yaml.safe_load" in src or "yaml.full_load" in src
    if not has_load:
        return 0, None
    return -30, (
        "CH001: lê catalog.yaml com yaml.safe_load directo. "
        "Refactor: `from library.ri import catalog` + `catalog.all_stocks(include_watchlist=True)` "
        "(ou `all_fiis`/`all_entries`/`all_tickers`)."
    )


def _check_ch002_stocks_only_loop(src: str, rel: str) -> tuple[int, str | None]:
    """Iterates only `stocks` section, missing watchlist_stocks."""
    if not RE_STOCKS_ONLY.search(src):
        return 0, None
    if RE_HAS_WATCHLIST.search(src):
        return 0, None
    if "catalog" not in src.lower():
        return 0, None
    return -25, (
        "CH002: lê só `stocks` section, ignora `watchlist_stocks`. "
        "Use `catalog.all_stocks(include_watchlist=True)`."
    )


def _check_ch003_fiis_only_loop(src: str, rel: str) -> tuple[int, str | None]:
    """Iterates only `fiis` section, missing watchlist_fiis."""
    if not RE_FIIS_ONLY.search(src):
        return 0, None
    if RE_HAS_WATCHLIST.search(src):
        return 0, None
    if "catalog" not in src.lower():
        return 0, None
    return -15, (
        "CH003: lê só `fiis` section, ignora `watchlist_fiis` (vulnerável quando watchlist crescer). "
        "Use `catalog.all_fiis(include_watchlist=True)`."
    )


def _check_ch004_dead_catalog_const(src: str, rel: str) -> tuple[int, str | None]:
    """CATALOG = .../catalog.yaml definido mas nunca usado no ficheiro."""
    m = RE_CATALOG_PATH_CONST.search(src)
    if not m:
        return 0, None
    name = m.group(1)
    # count usages excluding the definition line
    body_after_def = src[m.end():]
    if name in body_after_def:
        return 0, None
    return -10, (
        f"CH004: constante `{name}` definida mas nunca referenciada. "
        "Remover (cruft de refactor incompleto)."
    )


RE_OLLAMA_DIRECT_POST = re.compile(
    r'requests\.post\([^)]*(?:OLLAMA|"http://localhost:11434/api/generate"|'
    r"'http://localhost:11434/api/generate')",
    re.M | re.S,
)
RE_BARE_EXCEPT = re.compile(r'^\s*except\s*(?:Exception\s*)?:\s*(?:#.*)?$', re.M)
RE_AD_HOC_SECTION_BANNER = re.compile(
    r"print\(\s*f?[\"']\s*\\n\s*\{\s*['\"]=['\"]\s*\*\s*\d+\s*\}",
)


def _check_ch005_ollama_direct(src: str, rel: str) -> tuple[int, str | None]:
    """Hard-coded ollama POST without the canonical wrapper."""
    if rel in ALLOWLIST_OLLAMA_DIRECT:
        return 0, None
    if not RE_OLLAMA_DIRECT_POST.search(src):
        return 0, None
    return -20, (
        "CH005: requests.post directo a /api/generate. "
        "Refactor: `from agents._llm import ollama_call` + "
        "ollama_call(prompt, model=..., temperature=..., seed=...)."
    )


def _check_ch006_silent_except(src: str, rel: str) -> tuple[int, str | None]:
    """Bare `except:` or `except Exception:` with no log/raise inside.
    Quick heuristic: the next non-blank line is `pass` or `continue`.
    """
    if rel in ALLOWLIST_BARE_EXCEPT:
        return 0, None
    silent = 0
    for m in RE_BARE_EXCEPT.finditer(src):
        # Look at next 1-2 non-blank lines after the except: line.
        tail = src[m.end():].splitlines()[:3]
        nonblank = [ln.strip() for ln in tail if ln.strip()]
        if nonblank and nonblank[0] in ("pass", "continue"):
            silent += 1
    if silent == 0:
        return 0, None
    return -5 * min(silent, 3), (
        f"CH006: {silent} silent `except` swallowing errors. "
        "At minimum log the exception (logging.exception or print) so failures aren't invisible."
    )


def _check_ch007_ad_hoc_banner(src: str, rel: str) -> tuple[int, str | None]:
    """Ad-hoc print(f'\\n{...=*60...}== ...) banner instead of agents._common.section."""
    if rel in ALLOWLIST_AD_HOC_BANNER:
        return 0, None
    if not RE_AD_HOC_SECTION_BANNER.search(src):
        return 0, None
    return -8, (
        "CH007: ad-hoc section banner. Use "
        "`from agents._common import section as _section` + `_section('LABEL')`."
    )


# ---------------------------------------------------------------------------
# CH008 — file length
# ---------------------------------------------------------------------------

# Sourced from anthropics/claude-code-security-review
# .claude/commands/security-review.md (~18 categories). The list below
# documents the hard-exclusion categories: findings in these categories should
# NOT be raised as actionable security issues without additional exploit path
# evidence.  Used here as a seed constant for future wiring (no CH001-CH007
# changes).
# TODO: backfill verbatim strings from upstream prompt once the file is copied
#       to .claude/commands/security-review.md in this repo.
SKIP_PATTERNS: tuple[str, ...] = (
    "denial of service",                               # DoS without resource exhaustion proof
    "missing rate limit",                              # rate-limiting absent but no exploit
    "open redirect",                                   # redirect without phishing/token-leak context
    "log injection without sensitive data leak",       # log injection, no credential exposure
    "missing csrf for non-state-changing endpoints",   # CSRF on read-only endpoints
    "weak crypto without exploitation context",        # e.g. MD5 hash for non-auth use
    "verbose error messages",                          # stack traces without data leak
    "session timeout misconfiguration",                # long session but no exploit path
    "missing security headers without exploit path",   # CSP/X-Frame absent, no concrete attack
    "outdated dependency without known cve",           # version bump noise, no CVE assigned
    "use of http without tls in non-prod",             # http:// in dev/test configs
    "race conditions without exploit path",            # TOCTOU without demonstrated impact
    "lack of hsts",                                    # HSTS missing but no downgrade proof
    "missing captcha",                                 # captcha absent without automated-abuse evidence
    "weak password policy",                            # policy gap without account-takeover path
    "mfa missing",                                     # MFA not enforced, no privilege escalation path
    # TODO: backfill remaining 2 categories from upstream security-review.md
)

# Paths that CH008 should NOT flag (auto-generated / bundled output).
CH008_SKIP_PREFIXES = (
    "obsidian_vault/skills/design.lint_mega/",
    "mission-control/.next/",
)

CH008_LINE_LIMIT = 500


def _count_source_lines(src: str) -> int:
    """Count non-blank, non-pure-comment lines."""
    count = 0
    for line in src.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count


def _check_ch008_file_length(src: str, rel: str) -> tuple[int, str | None]:
    """File > 500 source lines — soft warning, no auto-fix."""
    for prefix in CH008_SKIP_PREFIXES:
        if rel.startswith(prefix):
            return 0, None
    n = _count_source_lines(src)
    if n <= CH008_LINE_LIMIT:
        return 0, None
    return -5, (
        f"CH008: {rel} is {n} source lines — consider splitting "
        f"(Anthropic best practice <{CH008_LINE_LIMIT}). "
        "Review if a function-extraction or sub-module would help."
    )


CHECKS = [
    _check_ch001_direct_catalog_load,
    _check_ch002_stocks_only_loop,
    _check_ch003_fiis_only_loop,
    _check_ch004_dead_catalog_const,
    _check_ch005_ollama_direct,
    _check_ch006_silent_except,
    _check_ch007_ad_hoc_banner,
    _check_ch008_file_length,
]


def _scan(src: str, rel: str) -> tuple[int, list[str], str | None]:
    """Returns (total_deduction, flag_list, primary_action_hint)."""
    deduction = 0
    flags: list[str] = []
    primary_hint: str | None = None
    for fn in CHECKS:
        delta, hint = fn(src, rel)
        if delta < 0 and hint:
            deduction += delta
            flags.append(hint.split(":", 1)[0])  # CH001, CH002, ...
            if primary_hint is None:
                primary_hint = hint
    return deduction, flags, primary_hint


class CodeHealthPerpetuum(BasePerpetuum):
    name = "code_health"
    description = "Detecta anti-patterns no codebase (catalog loops, dead constants, ...)"
    autonomy_tier = "T1"
    drop_alert_threshold = 15
    action_score_threshold = 70

    def subjects(self) -> list[PerpetuumSubject]:
        out = []
        for d in SCAN_DIRS:
            base = ROOT / d
            if not base.exists():
                continue
            for py in base.rglob("*.py"):
                if "__pycache__" in py.parts:
                    continue
                rel = str(py.relative_to(ROOT)).replace("\\", "/")
                if rel in ALLOWLIST_PATHS:
                    continue
                out.append(PerpetuumSubject(
                    id=f"code:{rel}",
                    label=rel,
                    metadata={"path": rel},
                ))
        return out

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        rel = subject.metadata["path"]
        path = ROOT / rel
        try:
            src = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return PerpetuumResult(
                subject_id=subject.id,
                score=-1,
                flags=[f"unreadable: {e}"],
            )

        deduction, flags, hint = _scan(src, rel)
        score = max(0, 100 + deduction)
        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(flags),
            flags=flags,
            details={"deduction": deduction, "rel_path": rel},
            action_hint=hint,
        )
