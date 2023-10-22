#!/bin/bash
cd src
python3 -m venv env
source env/bin/activate
pip install -r requirements.dev.txt
pip install GitPython
cd ..
clear
python make/run.py
deactivate
clear
rm -Rf src/env
rm -Rf make
rm -f cd.yml
echo "\033[1mYour Django project is ready to go!\033[0m"
echo "Visit https://github.com/jefgodesky/django-starter/wiki for ideas on next steps."
rm -- "$0"
