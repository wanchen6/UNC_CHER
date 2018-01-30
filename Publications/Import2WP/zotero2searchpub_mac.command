#!/usr/bin/env bash
#Finds this script directory and runs python3 on "NewsUpdateQualtrics_v24.py"
cd "$(dirname ${BASH_SOURCE[0]})"
SCRIPTFILE="zotero2searchpub_body.py"
INPUT="input.csv"
OUTPUT="output.xml"
python3 "$SCRIPTFILE" "$INPUT" "$OUTPUT"
