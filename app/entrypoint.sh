#!/bin/ash

# Wait for the Elasticsearch container to be ready before starting Kibana.
echo "Stalling for Elasticsearch"
while true; do
    nc elasticsearch 9200 2>/dev/null && break
done

echo "Starting app"
exec /usr/local/bin/python2 /app/manage.py server
