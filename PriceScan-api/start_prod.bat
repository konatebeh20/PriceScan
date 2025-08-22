@echo off
echo =====================================
echo   PRICESCAN API - MODE PRODUCTION
echo =====================================
echo.

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo Lancement en mode production...
python manage.py prod

pause
