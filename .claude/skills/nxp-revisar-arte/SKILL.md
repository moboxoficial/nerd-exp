---
name: nxp-revisar-arte
description: Revisão crítica (QA) de artes, legendas e vídeos do Nerd Experience / NerdVerso contra a identidade visual, a voz da marca e os fatos do evento. Use quando o usuário mandar uma imagem, print, link de página do Canva ou texto e pedir "revisa", "tá no padrão?", "confere essa arte", "tem erro?", "aprova?" para o NXP.
---

# Revisar arte NXP

Pré-requisito: skill **nxp-especialista** carregada (use `references/13-checklist-qa.md`, `03-cores.md`, `04-tipografia.md`, `07-voz-e-copy.md`).

## Como revisar

1. **Obtenha a peça**: imagem anexada, ou via Canva MCP (`read-design` com `design_content` + `thumbnails` da página indicada).
2. **Transcreva o texto** da arte exatamente como está (é aqui que aparecem os erros de digitação).
3. **Rode o checklist** completo (Informação, Ortografia, Identidade, Formato, Legenda, Acessibilidade).
4. **Classifique cada problema**:
   - 🔴 **Bloqueante** — informação errada (data/preço/nome), erro de ortografia, texto de template esquecido, logo ausente/distorcido, texto fora da zona segura.
   - 🟡 **Ajuste** — hierarquia fraca, mais de 2 cores de destaque, excesso de texto, pouco contraste, falta de CTA.
   - 🟢 **Sugestão** — melhorias de impacto (gancho, composição, elemento de marca).

## Formato da resposta

```
Veredito: ✅ Aprovado | ⚠️ Aprovado com ajustes | ❌ Reprovado

🔴 Bloqueantes
- [o quê] → [correção exata]

🟡 Ajustes
- …

🟢 Sugestões
- …

Texto corrigido da arte (se houver mudança):
…
```

Se estiver usando o Canva MCP e o usuário pedir, registre os bloqueantes como comentário na página (`comment-on-design`). Não edite a arte sem autorização explícita.
