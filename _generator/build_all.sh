#!/usr/bin/env sh
# Redraws the static SVGs in ../assets. Edit text/numbers in the .py files, then: sh build_all.sh
# (contrib.svg is redrawn by the Night Shift workflow from live GitHub data)
cd "$(dirname "$0")" && for f in hero report exhibits rest night; do python3 "$f.py"; done
