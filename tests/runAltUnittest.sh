#!/bin/sh

export KISSUT_CFG_FILE="tests/altConfig.json"
python -m unittest discover -s tests/
