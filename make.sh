#!/bin/bash
cd src
python3 -m venv env
source env/bin/activate
pip install -r requirements.dev.txt
pip install GitPython
cd ..
clear
python make.py
deactivate
clear
rm -Rf src/env
rm -f make.py
rm -f cd.yml
echo "Your Django project is ready to go!"
echo "Visit https://github.com/jefgodesky/django-starter/wiki for ideas on next steps."
rm -- "$0"
