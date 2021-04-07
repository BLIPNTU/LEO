#!/usr/bin/python3

# Required packages must be installed first
# pip command:
# pip install -r requirements.txt
#
# More information: https://packaging.python.org/key_projects/#pip

import blipleo
leo = blipleo.read_json('./data/baby_test.json')
blipleo.generate_leo(leo, './data')
