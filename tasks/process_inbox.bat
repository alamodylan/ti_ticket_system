@echo off

cd /d C:\SISTEMAS\ti_ticket_system

echo ================================ >> logs\process_inbox.log
echo EJECUCION: %date% %time% >> logs\process_inbox.log

C:\Users\usuario\AppData\Local\Programs\Python\Python312\python.exe tasks\process_inbox.py >> logs\process_inbox.log 2>&1

echo FIN EJECUCION: %date% %time% >> logs\process_inbox.log
echo ================================ >> logs\process_inbox.log
echo. >> logs\process_inbox.log