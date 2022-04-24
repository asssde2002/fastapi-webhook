#!/bin/sh

sh wait-for-postgres.sh db
/root/venv/bin/python main.py
