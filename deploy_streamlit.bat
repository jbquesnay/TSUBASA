# 🚀 Script de Déploiement Rapide

@echo off
echo ========================================
echo DEPLOIEMENT STREAMLIT CLOUD
echo ========================================
echo.

:: Vérifier si Git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Git n'est pas installe
    echo.
    echo Installer Git depuis: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/6] Verification des fichiers...
if not exist dashboard.py (
    echo [ERREUR] dashboard.py introuvable
    pause
    exit /b 1
)
if not exist requirements.txt (
    echo [ERREUR] requirements.txt introuvable
    pause
    exit /b 1
)
echo     OK - Tous les fichiers présents

echo.
echo [2/6] Creation de .gitignore...
if not exist .gitignore (
    (
        echo trade_history.json
        echo cumulative_data.json
        echo *.pkl
        echo __pycache__/
        echo .env
        echo venv/
    ) > .gitignore
    echo     OK - .gitignore cree
) else (
    echo     OK - .gitignore existe deja
)

echo.
echo [3/6] Initialisation Git...
if not exist .git (
    git init
    echo     OK - Git initialise
) else (
    echo     OK - Git deja initialise
)

echo.
echo [4/6] Ajout des fichiers...
git add dashboard.py config.yaml requirements.txt .gitignore
git add DASHBOARD_README.md DEPLOIEMENT_STREAMLIT_CLOUD.md
echo     OK - Fichiers ajoutes

echo.
echo [5/6] Commit initial...
git commit -m "Initial commit: Dashboard Streamlit ROYCE ROLLS"
if errorlevel 1 (
    echo     INFO - Aucun changement a commiter (deja fait)
) else (
    echo     OK - Commit effectue
)

echo.
echo ========================================
echo PROCHAINES ETAPES MANUELLES:
echo ========================================
echo.
echo 1. CREER UN REPO GITHUB:
echo    - Aller sur https://github.com/new
echo    - Nom: royce-rolls-dashboard
echo    - Public (requis pour Streamlit gratuit)
echo    - NE PAS ajouter README/gitignore
echo    - Cliquer "Create repository"
echo.
echo 2. LIER LE REPO (copier-coller):
echo    git remote add origin https://github.com/VOTRE_USERNAME/royce-rolls-dashboard.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. DEPLOYER SUR STREAMLIT:
echo    - Aller sur https://share.streamlit.io
echo    - Se connecter avec GitHub
echo    - Cliquer "New app"
echo    - Selectionner votre repo
echo    - Main file: dashboard.py
echo    - Cliquer "Deploy"
echo.
echo 4. VOTRE DASHBOARD SERA EN LIGNE:
echo    https://VOTRE_USERNAME-royce-rolls-dashboard.streamlit.app
echo.
echo ========================================
echo NOTES IMPORTANTES:
echo ========================================
echo.
echo - Remplacer VOTRE_USERNAME par votre nom GitHub
echo - Le deploiement prend 1-2 minutes
echo - L'app sera accessible depuis n'importe ou
echo - HTTPS securise automatique
echo - Gratuit et illimite!
echo.
echo ========================================

pause

