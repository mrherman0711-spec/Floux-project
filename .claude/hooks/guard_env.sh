#!/bin/bash
# PreToolUse hook — bloquea ediciones a .env (Twilio, OpenAI, Google, Evolution).
# Exit 2 = bloquear y explicar a Claude.

INPUT=$(cat)
FILE_PATH=$(printf '%s' "$INPUT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
")

[ -z "$FILE_PATH" ] && exit 0

case "$FILE_PATH" in
  *.env.example) exit 0 ;;
  *.env)
    echo "BLOQUEADO por hook: $FILE_PATH contiene secretos de producción (Twilio/OpenAI/Google/Evolution). Editalo a mano en la terminal." >&2
    exit 2 ;;
esac

exit 0
