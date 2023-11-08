#!/bin/sh
DJANGO_TESTING=1 COVERAGE_RCFILE=.coveragerc pytest -n auto .
