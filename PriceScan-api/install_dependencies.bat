@echo off
echo ========================================
echo   PRICESCAN-API - INSTALLATION
echo ========================================
echo.

echo [1/4] Verification de Python...
python --version
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

echo.
echo [2/4] Creation de l'environnement virtuel...
if not exist "venv" (
    python -m venv venv
    echo Environnement virtuel cree avec succes
) else (
    echo Environnement virtuel existe deja
)

echo.
echo [3/4] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo [4/4] Installation des dependances...
echo Installation des dependances principales...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo   INSTALLATION TERMINEE !
echo ========================================
echo.
echo Pour activer l'environnement virtuel:
echo   venv\Scripts\activate.bat
echo.
echo Pour lancer l'API:
echo   python app.py
echo.
pause
