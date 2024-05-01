#!/bin/bash

# Install Flask
pip install Flask

# Checking Flask installation
flask --version

# Starting flash app
python3 app.py

python3 -m pdoc *.py 