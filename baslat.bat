@echo off
start cmd /k "cd order_service && python app.py"
start cmd /k "cd logistics_service && python app.py"
start cmd /k "cd dashboard_service && python app.py"