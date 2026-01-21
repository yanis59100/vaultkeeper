@echo off
REM Script pour créer l'installateur Windows .EXE
REM Exécution: Double-clic ou: build_installer.bat

setlocal enabledelayedexpansion

echo.
echo ========== Creation Installateur Windows ==========
echo.

REM Vérifier Python
echo [1/3] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou accessible
    echo.
    echo Telecharge Python depuis: https://www.python.org/downloads/
    echo IMPORTANT: Coche "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Installer PyInstaller si nécessaire
echo [2/3] Installation de PyInstaller...
python -m pip install --quiet pyinstaller 2>nul
if errorlevel 1 (
    echo ERREUR: Impossible d'installer PyInstaller
    pause
    exit /b 1
)

REM Créer l'installateur
echo [3/3] Creation de l'installateur.exe...
python build_installer.py
if errorlevel 1 (
    echo ERREUR lors de la creation
    pause
    exit /b 1
)

echo.
echo ========== SUCCES ! ==========
echo.
echo Installateur cree: dist\PasswordManagerInstaller.exe
echo.
echo Prochaines etapes:
echo   1. Copie PasswordManagerInstaller.exe sur le Bureau
echo   2. Double-clic pour lancer l'installation
echo   3. Clique sur "Installer"
echo.
pause
