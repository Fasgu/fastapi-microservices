#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z host.docker.internal 5433; do
    sleep 0.1
done
echo "PostgreSQL started"
exec "$@"