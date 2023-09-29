#!/bin/bash
cd src
python3 -m venv env
source env/bin/activate
pip install -r requirements.dev.txt
cd ..
clear
python make.py
exit
clear
rm -Rf env
rm -f make.py
rm -- "$0"
