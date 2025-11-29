#!/bin/bash
DIR=${1:-'/StaticSiteGenerator/'}
python3 src/main.py "$DIR"
cd docs && python3 -m http.server 8888
