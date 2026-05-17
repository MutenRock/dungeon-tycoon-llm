#!/usr/bin/env bash
set -e
uvicorn backend.app.main:app --reload
