#!/usr/bin/env bash
set -euo pipefail

# Scripts directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STRICT="${STRICT:-0}"
EXIT_CODE=0

echo "==> Verificando versiones del entorno..."

# 1. Verificar Hugo
HUGO_VERSION_FILE="$ROOT_DIR/.hugo-version"
if [[ ! -f "$HUGO_VERSION_FILE" ]]; then
  echo "❌ Error: No se encuentra el fichero .hugo-version en $ROOT_DIR"
  exit 1
fi
EXPECTED_HUGO="$(tr -d '[:space:]' < "$HUGO_VERSION_FILE")"

if ! command -v hugo >/dev/null 2>&1; then
  echo "❌ Hugo no está instalado en el PATH."
  echo "   Sugerencia: brew install hugo"
  EXIT_CODE=1
else
  HUGO_RAW="$(hugo version)"
  # Ejemplo hugo version: hugo v0.169.0+extended+withdeploy darwin/arm64 ...
  ACTUAL_HUGO="$(echo "$HUGO_RAW" | sed -nE 's/.*v([0-9]+\.[0-9]+\.[0-9]+).*/\1/p')"
  
  if [[ "$HUGO_RAW" != *"+extended"* ]]; then
    echo "⚠️  ADVERTENCIA: Se recomienda la versión 'extended' de Hugo para Blowfish."
  fi

  if [[ "$ACTUAL_HUGO" != "$EXPECTED_HUGO" ]]; then
    echo "⚠️  Desfase en Hugo:"
    echo "   Esperada (.hugo-version): $EXPECTED_HUGO"
    echo "   Actual en PATH:           ${ACTUAL_HUGO:-desconocida}"
    echo "   Sugerencia: brew upgrade hugo (o actualizar .hugo-version si es intencionado)"
    if [[ "$STRICT" == "1" ]]; then
      EXIT_CODE=1
    fi
  else
    echo "✅ Hugo coincide: v$ACTUAL_HUGO (esperada: $EXPECTED_HUGO)"
  fi
fi

# 2. Verificar Go
GO_MOD_FILE="$ROOT_DIR/go.mod"
if [[ -f "$GO_MOD_FILE" ]]; then
  EXPECTED_GO="$(grep -E '^go [0-9]+\.[0-9]+(\.[0-9]+)?' "$GO_MOD_FILE" | awk '{print $2}')"
  if ! command -v go >/dev/null 2>&1; then
    echo "❌ Go no está instalado en el PATH."
    echo "   Sugerencia: brew install go"
    EXIT_CODE=1
  else
    ACTUAL_GO="$(go version | awk '{print $3}' | sed 's/^go//')"
    
    # Función para comparar versiones semánticas (>=)
    version_ge() {
      printf '%s\n%s\n' "$2" "$1" | sort -V -C
    }

    if version_ge "$ACTUAL_GO" "$EXPECTED_GO"; then
      echo "✅ Go es compatible: $ACTUAL_GO (requerida por go.mod: >= $EXPECTED_GO)"
    else
      echo "⚠️  Desfase en Go:"
      echo "   Requerida (go.mod): >= $EXPECTED_GO"
      echo "   Actual en PATH:       $ACTUAL_GO"
      echo "   Sugerencia: brew upgrade go"
      if [[ "$STRICT" == "1" ]]; then
        EXIT_CODE=1
      fi
    fi
  fi
fi

if [[ $EXIT_CODE -ne 0 ]]; then
  echo "❌ Falló la verificación de versiones (STRICT=$STRICT)."
  exit $EXIT_CODE
else
  echo "🎉 Todas las versiones están alineadas."
fi
