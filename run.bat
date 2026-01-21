@echo off
REM Gestionnaire de Mots de Passe - Lanceur Windows
REM Change vers le répertoire du script
cd /d "%~dp0"

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo Erreur: Python n'est pas installé
    echo ========================================
    echo.
    echo Veuillez télécharger Python 3.7+ depuis:
    echo https://www.python.org/downloads/
    echo.
    echo Lors de l'installation, COCHEZ:
    echo [x] Add Python to PATH
    echo.
    pause
    exit /b 1
)

REM Vérifier si cryptography est installé
python -c "import cryptography" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo Installation des dépendances...
    echo ========================================
    python -m pip install --user cryptography
    if errorlevel 1 (
        echo Erreur lors de l'installation de cryptography
        pause
        exit /b 1
    )
)

REM Lancer l'application
echo.
echo ========================================
echo Lancement du gestionnaire de mots de passe
echo ========================================
echo.
python main.py
pause

