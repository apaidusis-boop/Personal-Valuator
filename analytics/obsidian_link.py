"""Helpers para emitir URLs `obsidian://` clicáveis no terminal.

Windows Terminal (e Claude Code, VS Code Terminal, Wezterm, Alacritty)
reconhecem `obsidian://...` como link clicável e disparam o protocolo
registado pelo instalador do Obsidian — abre directo no app, sem
depender da associação default de `.md` no Windows.

Uso típico:

    from analytics.obsidian_link import vault_url, print_saved
    print_saved(vault_path)              # imprime path + URL clicável
    url = vault_url(vault_path)          # só o URL
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

VAULT_NAME = "obsidian_vault"


def _vault_root() -> Path:
    env = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env:
        return Path(env).resolve()
    return (Path(__file__).resolve().parent.parent / "obsidian_vault").resolve()


def vault_url(path: str | Path) -> str | None:
    """Converte um path (abs ou relativo ao repo/vault) em `obsidian://open?...`.

    Devolve None se o path não estiver dentro do vault — assim o caller
    pode cair no print plain sem branching.
    """
    root = _vault_root()
    p = Path(path)
    abs_p = p.resolve() if p.is_absolute() else (Path.cwd() / p).resolve()
    try:
        rel = abs_p.relative_to(root)
    except ValueError:
        return None
    encoded = quote(str(rel).replace("\\", "/"), safe="/")
    return f"obsidian://open?vault={quote(VAULT_NAME)}&file={encoded}"


def print_saved(path: str | Path, prefix: str = "[saved]") -> None:
    """Imprime `prefix path` e (se aplicável) a linha `obsidian://...` clicável."""
    print(f"{prefix} {path}")
    url = vault_url(path)
    if url:
        print(f"        {url}")
