# desktop — Helena Path B (Tauri)

Desktop app que apresenta o investment-intelligence como produto nativo
(Windows .exe / macOS .app), reusando 100% do backend Python via FastAPI sidecar.

> **Princípio**: Terminal = sala do chefe (CLI mantém-se intacta).
> Esta app é **o Escritório** — superfície polida e consumível.
> Ver `feedback_terminal_obsidian.md` na memória.

## Estado actual (Sprint 1 scaffold)

Já criado por `agents/helena_mega.py` autorização Path B:

```
desktop/
├── README.md                    ← este ficheiro
├── backend/
│   ├── main.py                  FastAPI app, health + meta + routers
│   ├── requirements.txt
│   ├── __init__.py
│   └── routers/
│       ├── __init__.py
│       ├── positions.py         /api/positions, /api/snapshot, /api/sectors
│       ├── ticker.py            /api/ticker/{sym}, /api/prices, /api/verdict
│       └── agents.py            /api/agents/list, /api/agents/run/{name}
└── src/
    ├── tokens.css               Helena Design System v1.0 → CSS custom properties
    ├── lib/
    │   ├── api.ts               TypeScript client to FastAPI
    │   └── plotly_theme.ts      Port of `ii_dark` Plotly template
    └── components/
        ├── KPITile.tsx          mirror de scripts/_components.py::kpi_tile
        ├── KPITile.css
        ├── StatusPill.tsx
        ├── SectionHeader.tsx
        └── AgentAttribution.tsx
```

**Falta ainda** (a fazer pelo founder OU próxima sessão Helena):
- `package.json` + `pnpm install` (precisa de Node.js + pnpm na máquina)
- `tauri.conf.json` + `cargo install tauri-cli` (precisa de Rust toolchain)
- React app entry (`main.tsx`, `App.tsx`)
- Routes (Portfolio, Ticker, Triggers, …)

## Pré-requisitos (instalar uma vez)

```bash
# Rust (para Tauri)
winget install --id Rustlang.Rustup -e

# Node.js + pnpm
winget install --id OpenJS.NodeJS -e
npm install -g pnpm

# Tauri CLI
cargo install tauri-cli --version "^2.0.0"
```

## Bootstrap completo (uma vez)

```bash
# 1. Backend Python deps
cd desktop/backend
python -m pip install -r requirements.txt

# 2. Smoke-test backend (para deve responder em :8765/api/health)
uvicorn desktop.backend.main:app --reload --port 8765
# em outro terminal:
curl http://127.0.0.1:8765/api/health
# expected: {"status":"ok","service":"helena-backend","version":"0.1.0"}

# 3. Scaffold Tauri + React frontend (via wizard)
cd ..
pnpm create tauri-app .
# Quando perguntar:
#   - Frontend language: TypeScript
#   - Package manager: pnpm
#   - UI framework: React
#   - UI flavor: Vite
#   - Project name: helena
# Importante: NÃO sobrescrever src/ que já existe — escolher outro nome
# ou mover src/ para src-keep/ antes, e copiar de volta depois.

# 4. Install deps + dev run
pnpm install
pnpm tauri dev
```

## Ciclo de desenvolvimento

```bash
# Terminal 1 — backend hot reload
uvicorn desktop.backend.main:app --reload --port 8765

# Terminal 2 — frontend hot reload (Tauri spawns Vite + opens webview)
cd desktop && pnpm tauri dev
```

## Production build

```bash
cd desktop
pnpm tauri build
# Output: src-tauri/target/release/bundle/msi/helena_X.X.X_x64_en-US.msi
# (~30MB Tauri shell + ~120MB total com PyInstaller backend bundle)
```

## API endpoints (já implementados)

| Endpoint | Método | Devolve |
|---|---|---|
| `/api/health` | GET | service status |
| `/api/meta` | GET | fx + holdings count + last price date |
| `/api/positions` | GET | active holdings BR+US com MV native |
| `/api/sectors` | GET | sector exposure em BRL (fx-converted) |
| `/api/snapshot?days=180` | GET | daily portfolio snapshots |
| `/api/ticker/{sym}` | GET | company + last price + latest score |
| `/api/prices/{sym}?days=365` | GET | OHLC time series |
| `/api/verdict/{sym}` | GET | verdict engine output |
| `/api/agents/list` | GET | agentes registados em config/agents.yaml |
| `/api/agents/run/{name}` | POST | dispara agent on-demand |

## Helena Design System

Todos os componentes em `src/components/` espelham o `scripts/_components.py`.
Tokens em `src/tokens.css` são tradução directa de `scripts/_theme.py::COLORS`.

**Regra**: se vais alterar token, alterar **ambos** os ficheiros simultaneamente.
Se vais introduzir cor/tipo nova, primeiro promover ao `Design_System.md` —
e só depois replicar nos dois lados.

## Sprint roadmap (estimativa Helena)

- **Sprint 1 (este)** — scaffold backend + tokens + componentes ✅
- **Sprint 2** — package.json + Tauri config + main.tsx + Portfolio route
- **Sprint 3** — Ticker route + Plotly.js charts + remaining components
- **Sprint 4** — System tray + native menu + sidecar packaging via PyInstaller + .msi installer

## Cross-links

- [`obsidian_vault/skills/Design_System.md`](../obsidian_vault/skills/Design_System.md)
- [`obsidian_vault/skills/Helena_Mega/03_Spikes.md`](../obsidian_vault/skills/Helena_Mega/03_Spikes.md) — spike completo Path B
- [`obsidian_vault/skills/Claude_Design_Integration.md`](../obsidian_vault/skills/Claude_Design_Integration.md) — prototyping flow
- [`scripts/_theme.py`](../scripts/_theme.py) — tokens canónicos source
- [`scripts/_components.py`](../scripts/_components.py) — componentes Streamlit source
