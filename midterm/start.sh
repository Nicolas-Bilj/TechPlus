#!/bin/bash

# Install Flask
pip install -r requirements.txt

# Checking Flask installation
flask --version

# Starting flash app
python3 app.py

python3 -m pdoc *.py 