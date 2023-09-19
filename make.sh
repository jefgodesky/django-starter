#!/bin/bash

poetry install
clear
poetry run python make.py
cd src
poetry install
cd ..
rm -f make.py
rm -f pyproject.toml
rm -f poetry.lock
rm -- "$0"
