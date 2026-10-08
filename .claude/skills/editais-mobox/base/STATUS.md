# Status da base

Última atualização: 2026-10-08

| Fonte | Link | Status |
|---|---|---|
| Planilha histórica de editais | https://docs.google.com/spreadsheets/d/1xMqwEDeqJjWKR2-W_FJ-K-_zp3NHrE7xEq6JJjxewfQ | **Não ingerida** — o conector do Google Drive não encontra o arquivo (conta conectada provavelmente não é a que tem acesso) e o link não é público. |
| Pasta do Drive de editais | https://drive.google.com/drive/folders/1T04BHmpVA-1Z3imE6r6KlfjW9eeVnDME | **Não ingerida** — busca/listagem de arquivos está desativada no conector do Google Drive. |
| IUPI (servidor MCP) | https://ikzfaykxlhwvtattlbri.supabase.co/functions/v1/mcp | **Não ingerida** — o servidor exige login OAuth; precisa ser adicionado como conector personalizado no claude.ai para as ferramentas aparecerem na sessão. |

## Projetos já conhecidos (fora das fontes acima)

- Nerd Experience (NXP / NerdXP Pop Festival) — mencionado nas skills de social
  media da Mobox; dados de edital/captação ainda não levantados.

## Ordem de ingestão planejada

1. Planilha histórica → `editais.md`, `proponentes.md`, `projetos.md` (esqueleto).
2. Drive, pasta por pasta → propostas aprovadas e reprovadas, pareceres,
   orçamentos → completar `projetos.md`, `equipes.md`, `licoes.md` e o
   "Estilo Mobox" em `references/estrutura-de-proposta.md`.
3. IUPI → conferir/atualizar status atuais.
