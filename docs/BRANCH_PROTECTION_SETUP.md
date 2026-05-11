# Branch protection — setup guide

> **Repo**: `apaidusis-boop/Personal-Valuator` · **Branch**: `main`
> **Pré-requisito**: workflows `test.yml` + `codeql.yml` já em `origin/main` (commit `d576c9d`).
> **Tempo**: ~2 min (UI) ou ~5 min (CLI).

---

## Por que isto agora

Sem branch protection, `git push origin main` chega a `main` sem qualquer gate. Os dois CI workflows (pytest + CodeQL) correm a cada push, mas o resultado é decorativo — falhas não bloqueiam nada. Activar protection torna os checks **required** e fecha 3 buracos:

- Push directo de código que parte testes.
- Force-push acidental que reescreve histórico de `main`.
- `git push --delete origin main` acidental.

Como és solo dev, **não** activamos required PR review (bloquearia merges directos). Só activamos status checks + force-push block + delete block.

---

## Path A — GitHub UI (recomendado, ~2 min)

1. Abrir o painel de regras:

   https://github.com/apaidusis-boop/Personal-Valuator/settings/rules

2. Clicar **"New ruleset" → "New branch ruleset"**.

3. **Ruleset name**: `main protection`.

4. **Enforcement status**: `Active`.

5. **Target branches**:
   - Add target → `Include default branch` (cobre `main` automaticamente mesmo se mudar de nome).

6. **Branch rules** (tick estes, só estes):

   | Rule | Setting | Por que |
   |---|---|---|
   | Restrict deletions | ✅ ON | Bloqueia `git push --delete origin main` |
   | Block force pushes | ✅ ON | Bloqueia `git push --force` que reescreve histórico |
   | Require status checks to pass | ✅ ON | Activa o gate dos workflows |
   | ↳ Require branches to be up to date before merging | ✅ ON | Impede merges em snapshots stale |
   | Require a pull request before merging | ⬜ OFF | Solo dev — bloquearia merges directos |
   | Require signed commits | ⬜ OFF | Tu não assinas; activar só quando configurares GPG |
   | Require linear history | ⬜ OFF | Já trabalhas linear de facto; rule é redundante |

7. **Status checks** (clicar **"Add checks"** depois de tickar a regra acima):
   - Adicionar `test` (job do `test.yml`)
   - Adicionar `Analyze (python)` (job do `codeql.yml`)

   Se algum não aparece na search box, é porque ainda não correu uma vez em `main`. Ver secção **Troubleshooting** abaixo.

8. **"Create"** no fim da página.

✅ **Done.**

---

## Path B — gh CLI (programático)

```powershell
# 1. Instalar gh (uma vez)
winget install --id GitHub.cli --silent

# 2. Auth (browser flow, uma vez)
gh auth login --hostname github.com --git-protocol https --web

# 3. Verificar
gh auth status

# 4. Aplicar ruleset (idempotente — re-run actualiza)
gh api -X POST /repos/apaidusis-boop/Personal-Valuator/rulesets `
  -H "Accept: application/vnd.github+json" `
  -F name="main protection" `
  -F target="branch" `
  -F enforcement="active" `
  -F "conditions[ref_name][include][]=~DEFAULT_BRANCH" `
  -F "rules[][type]=deletion" `
  -F "rules[][type]=non_fast_forward" `
  -F "rules[][type]=required_status_checks" `
  -F "rules[][parameters][strict_required_status_checks_policy]=true" `
  -F "rules[][parameters][required_status_checks][][context]=test" `
  -F "rules[][parameters][required_status_checks][][context]=Analyze (python)"
```

> Nota PowerShell 5.1: o backtick (`` ` ``) é continuation; `=` em `-F key=value` faz `gh` enviar como string. Para passar arrays usa `-F "key[][sub]=val"` repetidamente como acima.

---

## Verificação pós-setup

```powershell
# Lista rulesets activos
gh api /repos/apaidusis-boop/Personal-Valuator/rulesets

# Tentar force-push (deve falhar)
git push --force origin main
# → ! [remote rejected] main -> main (cannot force-push to this branch)

# Tentar push de commit que parte testes (deve falhar quando workflows correrem)
# (ou simplesmente confiar que os workflows correrão no próximo push)
```

Ou via UI: o teu próximo push para `main` mostra um amarelo ⏳ enquanto os workflows correm, e ✅/❌ no fim. Se ❌, o push pode ainda ter ido (rule de status check bloqueia *merge via PR*, não push directo). Para bloquear push directo, ver secção abaixo.

---

## Bloquear push directo (opcional, mais rigoroso)

Branch rulesets em modo `branch` aplicam a **PR merges**, não a `git push`. Se quiseres exigir PR para qualquer mudança em `main`:

1. Tickar **"Require a pull request before merging"** no ruleset.
2. Sub-opções:
   - Required approvals: `0` (solo).
   - Dismiss stale approvals: ON (cosmético sem reviewers, mas inofensivo).
   - Require approval of the most recent reviewable push: OFF.

Após isto, `git push origin main` directamente é rejeitado; tens que abrir PR (mesmo que self-merge). Trade-off: cada mudança custa 30s extra. Se preferires velocidade > rigor, deixa OFF.

---

## Troubleshooting

### "Status check name not found in search"

O check só aparece depois de ter corrido **pelo menos uma vez** no branch `main`. Se acabámos de fazer push das workflows, pode levar 1-2 min até CodeQL terminar. Refrescar a search box ou:

```powershell
# Forçar workflows a correr num push trivial
git commit --allow-empty -m "chore: trigger CI for branch protection setup"
git push origin main
# Esperar ~2 min, refrescar a UI
```

### Ruleset criado mas force-push ainda passa

Verificar enforcement status: tem que ser `Active` (não `Evaluate` que só regista sem bloquear).

```powershell
gh api /repos/apaidusis-boop/Personal-Valuator/rulesets `
  --jq '.[] | {name, enforcement}'
```

### Reverter (rollback)

Via UI: Settings → Rules → click no ruleset → **"Delete ruleset"**.

Via CLI:
```powershell
$RID = gh api /repos/apaidusis-boop/Personal-Valuator/rulesets `
       --jq '.[] | select(.name=="main protection") | .id'
gh api -X DELETE /repos/apaidusis-boop/Personal-Valuator/rulesets/$RID
```

---

## Próximos passos depois de activar

1. Próximo push de `daily_run.bat` (cron 23:30) corre os workflows. Confirmar que ambos passam (`test` + `Analyze (python)`).
2. Se `test` falhar em CI mas passar local, é porque as 4 test files têm dependências que o runner Ubuntu não tem (Ollama, Windows-specific paths). Editar `test.yml` para excluir ou marcar `xfail`.
3. Considerar adicionar terceiro check: `Helena audit` (correr `python -m agents.helena.audit` em CI; falha se `errors > 0`). Adia até `test` + `CodeQL` estabilizarem.

---

## Referências

- GitHub Rulesets docs: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets
- gh CLI ruleset reference: `gh api -X POST /repos/{owner}/{repo}/rulesets --help`
- Workflows shipped neste repo: `.github/workflows/test.yml` (commit `d576c9d`), `.github/workflows/codeql.yml` (commit `d576c9d`).
