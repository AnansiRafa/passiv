#!/bin/bash

echo "Starting Celery worker..."
celery -A passiv worker --loglevel=info
