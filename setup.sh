echo [*] creating local log file: ./sleep.log
touch sleep.log

echo [*] extracting login info from "last" command
echo [ ] more info: man last
last | python lastToLog.py

echo [+] no errors? ready to go!!
echo [ ] display table with: python lastTable.py
