@echo off
cd /d %~dp0
python zotero2searchpub_body.py input.csv output.xml %*
PAUSE