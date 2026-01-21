@echo off
REM Gestionnaire de Mots de Passe - Installation sur le Bureau Windows
REM Ce script installe l'application directement sur le Bureau

setlocal enabledelayedexpansion

echo.
echo ========== Gestionnaire de Mots de Passe ==========
echo Installation sur le BUREAU Windows
echo.
echo.

REM Vérifier les droits administrateur
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Ce script doit etre lance en tant qu'administrateur
    echo.
    echo Solution: Cliquez droit sur ce fichier et selectionnez
    echo "Executer en tant qu'administrateur"
    echo.
    pause
    exit /b 1
)

REM Vérifier Python
echo [VERIF] Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERREUR: Python n'est pas installe ou non accessible
    echo.
    echo Solutions:
    echo 1. Telecharge Python 3.7+ depuis: https://www.python.org/downloads/
    echo 2. Lors de l'installation, COCHE: "Add Python to PATH"
    echo 3. Redémarre l'ordinateur
    echo 4. Relance ce script
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo   OK - %PYTHON_VERSION%

REM Installer les dépendances
echo.
echo [INSTAL] Dependances...
python -m pip install --quiet --user cryptography pyinstaller 2>nul
if errorlevel 1 (
    echo.
    echo Installation des dependances avec --user echouee, essai normal...
    python -m pip install --quiet cryptography pyinstaller
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer les dependances
        pause
        exit /b 1
    )
)
echo   OK - cryptography installe
echo   OK - pyinstaller installe

REM Créer l'exécutable
echo.
echo [CREATE] Executable Windows...
echo (Cela peut prendre quelques minutes, veuillez patienter...)
python build_exe.py >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERREUR lors de la creation de l'executable
    echo Essayez manuellement:
    echo   pyinstaller main.py --name=PasswordManager --onefile --windowed
    pause
    exit /b 1
)

REM Vérifier l'exécutable
if not exist "dist\PasswordManager.exe" (
    echo ERREUR: L'executable n'a pas pu etre cree
    pause
    exit /b 1
)

echo   OK - PasswordManager.exe cree

REM Trouver le Bureau
echo.
echo [SETUP] Installation sur le Bureau...

for /f "tokens=3" %%i in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul ^| findstr Desktop') do set DESKTOP=%%i

if not defined DESKTOP (
    echo ERREUR: Bureau non trouve. Installation dans le dossier courant.
    set DESKTOP=%CD%
)

REM Créer un dossier sur le Bureau pour l'application
set APP_FOLDER=!DESKTOP!\Gestionnaire de Mots de Passe
if not exist "!APP_FOLDER!" (
    echo   Creation du dossier...
    mkdir "!APP_FOLDER!"
)

REM Copier l'exécutable sur le Bureau
echo   Copie de l'executable...
copy "dist\PasswordManager.exe" "!APP_FOLDER!\PasswordManager.exe" >nul
if errorlevel 1 (
    echo ERREUR lors de la copie
    pause
    exit /b 1
)

REM Copier les fichiers de données (s'ils existent)
echo   Copie des donnees...
if exist "salt.bin" copy "salt.bin" "!APP_FOLDER!\salt.bin" >nul 2>&1
if exist "passwords.enc" copy "passwords.enc" "!APP_FOLDER!\passwords.enc" >nul 2>&1

REM Créer un raccourci sur le Bureau (fichier .lnk)
echo   Creation d'un raccourci Bureau...

set SHORTCUT_PATH=!DESKTOP!\PasswordManager.lnk

(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "!SHORTCUT_PATH!"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "!APP_FOLDER!\PasswordManager.exe"
    echo oLink.WorkingDirectory = "!APP_FOLDER!"
    echo oLink.Description = "Gestionnaire de Mots de Passe Securise"
    echo oLink.IconLocation = "!APP_FOLDER!\PasswordManager.exe,0"
    echo oLink.Save
) > "!APP_FOLDER!\create_shortcut.vbs"

cscript //nologo "!APP_FOLDER!\create_shortcut.vbs"
del "!APP_FOLDER!\create_shortcut.vbs" 2>nul

REM Résumé
echo.
echo ========== INSTALLATION REUSSIE ==========
echo.
echo Dossier Bureau: !APP_FOLDER!
echo Executable: !APP_FOLDER!\PasswordManager.exe
echo Raccourci Bureau: !DESKTOP!\PasswordManager.lnk
echo.
echo UTILISATION:
echo   1) Double-cliquez sur "PasswordManager" sur le Bureau
echo   2) Ou ouvrez le dossier "Gestionnaire de Mots de Passe"
echo      et lancez PasswordManager.exe
echo.
echo CONSEILS:
echo   * Vous pouvez supprimer ce fichier (install.bat) apres installation
echo   * Epinglez l'application a la barre des taches
echo   * Dossier de donnees: !APP_FOLDER!
echo     - salt.bin (cle de chiffrement)
echo     - passwords.enc (mots de passe chiffres)
echo   * Sauvegardez ces fichiers regulierement !
echo.
pause
