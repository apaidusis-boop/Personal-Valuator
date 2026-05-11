"""fetchers.subscriptions — paid subscription content ingest.

Adapters por site; todos herdam de `BaseAdapter` em `_base.py`.
Ver `obsidian_vault/wiki/playbooks/Web_scraping_subscriptions.md` para arquitetura.
"""
from ._base import BaseAdapter, AdapterResult, Report
from ._session import SessionManager, PlaywrightSession

__all__ = ["BaseAdapter", "AdapterResult", "Report", "SessionManager", "PlaywrightSession"]
