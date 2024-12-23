#!/usr/bin/env sh

python -m venv venv
./venv/bin/activate
pip install -r requirements.txt
python -m app
