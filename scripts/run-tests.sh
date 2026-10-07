#!/bin/bash

echo "Running all unit/e2e tests..."
python -m unittest discover -s tests -v || exit 1

echo ""
echo "Running coverage..."
python -m coverage run -m unittest discover -s tests || exit 1
python -m coverage report -m
python -m coverage html

echo ""
echo "SUCCESS"
echo "Coverage report: htmlcov/index.html"
