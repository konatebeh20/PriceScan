@echo off
echo ========================================
echo    PRICESCAN API - DEMARRAGE
echo ========================================
echo.

echo [1/5] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)
echo Python OK

echo.
echo [2/5] Verification de l'environnement virtuel...
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ERREUR: Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
)
echo Environnement virtuel OK

echo.
echo [3/5] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)
echo Environnement virtuel active

echo.
echo [4/5] Installation des dependances...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERREUR: Impossible d'installer les dependances
    pause
    exit /b 1
)
echo Dependances installees

echo.
echo [5/5] Demarrage de l'API...
echo.
echo L'API sera accessible sur: http://localhost:5000
echo Health check: http://localhost:5000/health
echo.
echo Appuyez sur Ctrl+C pour arreter l'API
echo.

python app.py

echo.
echo API arretee
pause
