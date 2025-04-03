#!/bin/bash
# wait-for-it.sh

set -e

host="$1"
shift
cmd="$@"

until curl -s "$host:9200/_cat/health?h=status" | grep -q "green\|yellow"; do
  >&2 echo "Elasticsearch está iniciando - esperando..."
  sleep 1
done

>&2 echo "Elasticsearch está listo - ejecutando comando"
exec $cmd
