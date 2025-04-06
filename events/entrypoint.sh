#!/bin/bash

poetry run python src/manage.py migrate --noinput

exec "$@"