#!/usr/bin/env bash
#Finds this script directory and runs python3 on "NewsUpdateQualtrics_v24.py"
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
SCRIPTFILE="/NewsUpdateQualtrics_v24.py"
python3 "$DIR$SCRIPTFILE"
