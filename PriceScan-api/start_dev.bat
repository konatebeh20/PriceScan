@echo off
echo =====================================
echo   PRICESCAN API - MODE DEVELOPPEMENT
echo =====================================
echo.

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo Lancement en mode developpement...
python manage.py dev

pause
