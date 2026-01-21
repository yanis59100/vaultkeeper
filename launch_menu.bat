@echo off
chcp 65001 > nul
cls

echo.
echo =====================================================
echo     GESTIONNAIRE DE MOTS DE PASSE v2.0
echo     Securise - Moderne - Facile a utiliser
echo =====================================================
echo.
echo Choix disponibles :
echo.
echo 1. Lancer l'application (PasswordManager.exe)
echo 2. Creer un raccourci sur le Bureau
echo 3. Reconstruire l'executable
echo 4. Afficher les informations de securite
echo 5. Quitter
echo.
set /p choice=Entrez votre choix (1-5) : 

if "%choice%"=="1" (
    echo.
    echo Lancement du Gestionnaire de Mots de Passe...
    echo.
    start "" ".\dist\PasswordManager.exe"
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Creation du raccourci sur le Bureau...
    call create_shortcut.bat
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Reconstruction de l'executable...
    python build_exe_modern.py
    goto end
)

if "%choice%"=="4" (
    echo.
    echo =====================================================
    echo     INFORMATIONS DE SECURITE
    echo =====================================================
    echo.
    echo CHIFFREMENT :
    echo   - Type : AES-256 avec Fernet
    echo   - Derivation : PBKDF2-SHA256
    echo   - Iterations : 480 000 (renforcees)
    echo   - Salt : 32 bytes aleatoires
    echo.
    echo STOCKAGE :
    echo   - Fichiers caches sur Windows
    echo   - Hash d'integrite pour chaque sauvegarde
    echo   - Verification automatique de corruption
    echo.
    echo PROTECTION :
    echo   - Mot de passe maitre : Minimum 6 caracteres
    echo   - Affichage optionnel des mots de passe
    echo   - Export securise en CSV
    echo.
    echo RECOMMANDATIONS :
    echo   - Utilisez un mot de passe maitre FORT et UNIQUE
    echo   - Ne l'ecrivez jamais nulle part
    echo   - Sauvegardez regulierement
    echo   - Si vous perdez le mot de passe maitre, vous perdrez TOUS VOS COMPTES
    echo.
    echo =====================================================
    pause
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo Au revoir !
    goto end
)

echo Choix invalide. Veuillez recommencer.
timeout /t 2
cls
goto menu

:menu
cls
goto start

:end
