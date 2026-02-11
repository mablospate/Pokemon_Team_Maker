#!/bin/sh

if [ -z "$SECRET_KEY" ]; then
  export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
fi

: "${DATABASE_URL:=sqlite:///pokemon.db}"
export DATABASE_URL

exec "$@"
