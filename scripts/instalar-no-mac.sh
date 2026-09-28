#!/usr/bin/env bash
# Instala o Especialista NXP globalmente no Claude Code do Mac (~/.claude),
# para funcionar em qualquer pasta, não só dentro deste repositório.
# Uso: ./scripts/instalar-no-mac.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

mkdir -p "$DEST/skills" "$DEST/agents" "$DEST/nxp-brand"

for skill in nxp-especialista nxp-criar-post nxp-revisar-arte nxp-planejar-campanha; do
  rm -rf "$DEST/skills/$skill"
  cp -R "$REPO/.claude/skills/$skill" "$DEST/skills/$skill"
  echo "✓ skill $skill"
done

cp "$REPO/.claude/agents/nxp-diretor-de-arte.md" "$DEST/agents/"
echo "✓ subagente nxp-diretor-de-arte"

# Documentação (README, guia de skills, instruções para Projeto do claude.ai)
rm -rf "$DEST/nxp-brand"
cp -R "$REPO/nxp-brand" "$DEST/nxp-brand"
echo "✓ documentação em $DEST/nxp-brand"

cat <<'EOF'

Pronto! Abra o Claude Code em qualquer pasta e peça, por exemplo:
  "cria um post de feed anunciando o 2º lote do NXP"

Opcional — skills de terceiros (rode dentro do Claude Code):
  /plugin marketplace add anthropics/skills
  /plugin install example-skills@anthropic-agent-skills
  /plugin install document-skills@anthropic-agent-skills
  /plugin marketplace add coreyhaines31/marketingskills
  /plugin install marketing-skills@marketingskills

Ferramentas de vídeo/imagem:  brew install ffmpeg imagemagick
EOF
