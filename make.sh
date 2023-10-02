#!/bin/bash
cd src
python3 -m venv env
source env/bin/activate
pip install -r requirements.dev.txt
pip install GitPython
cd ..
clear
python make.py
exit
clear
rm -Rf src/env
rm -f make.py
rm -- "$0"
