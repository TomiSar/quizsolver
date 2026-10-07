#!/bin/bash

echo "Cleaning all unit/e2e test results..."
rm -rf __pycache__/
rm -rf htmlcov/
rm -rf tests/__pycache__/
rm -rf data/__pycache__/
rm -f .coverage
rm -f coverage.xml
echo "Cleaned all unit/e2e test results."
