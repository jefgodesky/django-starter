#!/bin/bash
cd src
python3 -m venv env
source env/bin/activate
pip install -r requirements.dev.txt
pip install inquirer
pip install GitPython
cd ..
clear
python make/run.py
deactivate
clear
rm -Rf src/env
rm -Rf make
rm -f cd.yml
echo "${bold}Your Django project is ready to go!${normal}"
echo "Visit https://github.com/jefgodesky/django-starter/wiki for ideas on next steps."
rm -- "$0"
