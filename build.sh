#!/bin/bash
# build.sh - This runs on Render during deployment

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --settings=safeyouth_api.settings_production

# Collect static files
python manage.py collectstatic --noinput --settings=safeyouth_api.settings_production