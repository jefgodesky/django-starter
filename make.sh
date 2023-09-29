#!/bin/bash
cd src
pip install -r requirements.dev.txt
clear
python make.py
rm -f make.py
rm -- "$0"
