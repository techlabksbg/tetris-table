@echo on
powershell.exe -ExecutionPolicy Bypass -Command "cat %1 | python.exe .\toBitMap.py"