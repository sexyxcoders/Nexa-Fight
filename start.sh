#!/bin/bash
pip3 install -r requirements.txt --quiet
mkdir -p nexa Nexa assets
touch nexa/__init__.py Nexa/data.py
bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/Nexa/main/setup.sh)
python3 main.py
