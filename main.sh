#!/bin/bash
DIR=${1:-'/StaticSiteGenerator/'}
python3 src/main.py "$DIR"
cd docs && python3 -m http.server 8888
if [ "$BASEPATH" = "/" ]; then
    echo "Running local server at http://0.0.0.0:8888"
    cd docs && python3 -m http.server 8888
else
    echo "Base path is not '/', skipping local server."
    echo "Generated site is in docs/ folder, ready for deployment."
fi