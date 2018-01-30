#!/usr/bin/env bash
#Finds this script directory and runs python3 on "NewsUpdateQualtrics_v24.py"
cd "$(dirname ${BASH_SOURCE[0]})"
SCRIPTFILE="NewsUpdateQualtrics_v24.py"
python3 "$SCRIPTFILE"
