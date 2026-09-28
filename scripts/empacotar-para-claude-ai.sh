#!/usr/bin/env bash
# Gera .zip de cada skill NXP para upload no claude.ai / app Claude
# (Configurações → Capacidades → Skills → Upload skill).
# Uso: ./scripts/empacotar-para-claude-ai.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO/dist/claude-ai"
mkdir -p "$OUT"

for skill in nxp-especialista nxp-criar-post nxp-revisar-arte nxp-planejar-campanha; do
  rm -f "$OUT/$skill.zip"
  (cd "$REPO/.claude/skills" && zip -qr "$OUT/$skill.zip" "$skill" -x '*.DS_Store')
  echo "✓ $OUT/$skill.zip"
done

echo
echo "Faça upload primeiro do nxp-especialista.zip (as outras dependem dele)."
