---
name: editais-mobox
description: Cérebro de editais, projetos e propostas da Mobox Produções e empresas parceiras. Use sempre que o pedido envolver edital, chamada pública, lei de incentivo (Rouanet, LIC-MG, Lei Municipal BH, PNAB/Aldir Blanc, Paulo Gustavo, ProAC etc.), patrocínio incentivado, captação, proposta, projeto cultural, inscrição, prestação de contas, proponente, CNPJ proponente, equipe técnica/ficha técnica, orçamento de projeto, contrapartidas, recurso de resultado, ou quando perguntarem "temos projeto pra esse edital?", "qual empresa inscreve?", "por que perdemos X?", "escreve a justificativa", "monta a proposta".
---

# Editais Mobox — o cérebro

Esta skill concentra tudo o que a Mobox e as empresas parceiras já escreveram,
inscreveram, aprovaram e perderam em editais, e transforma isso em método.

## Antes de qualquer coisa

1. Leia `base/STATUS.md` para saber o que já foi ingerido das fontes
   (planilha antiga, Drive de editais, IUPI) e o que ainda falta.
2. Para qualquer fato sobre a Mobox (proponente, CNPJ, valores aprovados,
   equipe, resultado de edital), use **somente** o que está em `base/`.
   Se não estiver lá, diga que não está na base e pergunte — nunca invente
   número, nome, CNPJ, data ou resultado.
3. Para regras de um edital específico, a fonte é o texto do edital vigente.
   `references/mecanismos-de-fomento.md` é só orientação geral: confirme
   prazos, tetos, percentuais e documentos no edital antes de afirmar.

## Mapa de arquivos

| Arquivo | O que tem |
|---|---|
| `base/STATUS.md` | Fontes, o que foi ingerido, pendências |
| `base/proponentes.md` | Empresas (Mobox + parceiras), CNPJs, naturezas jurídicas, cadastros, histórico, restrições |
| `base/projetos.md` | Portfólio de projetos: tipo, linguagem, formato, porte, status, onde já foi inscrito |
| `base/editais.md` | Histórico de inscrições: edital × projeto × proponente × resultado × nota |
| `base/equipes.md` | Pessoas e funções recorrentes, currículos-resumo, em quais projetos aparecem |
| `base/licoes.md` | Por que ganhamos, por que perdemos, pareceres, notas por critério |
| `references/fluxos.md` | Passo a passo de cada tarefa (triagem, fit, redação, revisão, pós-resultado) |
| `references/estrutura-de-proposta.md` | Seções padrão de proposta e como escrevê-las no estilo Mobox |
| `references/mecanismos-de-fomento.md` | Visão geral dos mecanismos de fomento mais usados |
| `references/taxonomia.md` | Vocabulário controlado: tipos de projeto, linguagens, portes, status, funções |

## Tarefas e qual fluxo seguir (detalhes em `references/fluxos.md`)

- **Chegou um edital novo** → Fluxo A (triagem): resumir regras, elegibilidade,
  prazos, teto, critérios de pontuação, documentos; cruzar com proponentes e
  projetos da base; recomendar *qual projeto* com *qual proponente*, ou dizer
  que não vale a pena e por quê.
- **"Temos projeto pra isso?" / "qual empresa inscreve?"** → Fluxo B (fit).
- **Escrever ou adaptar proposta** → Fluxo C (redação), sempre partindo de
  textos aprovados da base para o mesmo tipo de projeto.
- **Revisar proposta antes de enviar** → Fluxo D (revisão contra critérios
  do edital + erros já cometidos em `base/licoes.md`).
- **Saiu resultado** → Fluxo E (pós-resultado): registrar em `base/editais.md`,
  extrair lições para `base/licoes.md`, avaliar recurso.

## Regras de ouro

- Pontue contra a tabela de critérios do edital, item a item. Proposta boa
  que não responde ao critério perde ponto.
- Proponente certo importa tanto quanto o projeto: confira natureza jurídica,
  CNAE/atuação, tempo de existência, sede, limites de projetos simultâneos,
  pendências e se a empresa já foi contemplada no mesmo edital.
- Reaproveite o que já foi aprovado, mas reescreva para o edital da vez —
  avaliador percebe texto genérico.
- Ao aprender algo novo (resultado, parecer, padrão de escrita), atualize a
  base no mesmo passo e registre a origem (arquivo/link e data).
