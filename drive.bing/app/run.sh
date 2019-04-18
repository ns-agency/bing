#!/usr/bin/env bash

gunicorn bing_drive:app -b 0.0.0.0:8000
