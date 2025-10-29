# 🚀 Script de Déploiement Streamlit Cloud

@echo off
echo ========================================
echo DEPLOIEMENT DASHBOARD STREAMLIT CLOUD
echo ========================================
echo.

:: Vérifier si Git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Git n'est pas installe
    echo.
    echo Telecharger et installer Git:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [1/7] Verification des fichiers...
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
if not exist config.yaml (
    echo [ERREUR] config.yaml introuvable
    pause
    exit /b 1
)
echo     OK - Tous les fichiers dashboard presents

echo.
echo [2/7] Verification/Creation de .gitignore...
if not exist .gitignore (
    (
        echo trade_history.json
        echo cumulative_data.json
        echo *.pkl
        echo __pycache__/
        echo .env
        echo venv/
        echo *.log
    ) > .gitignore
    echo     OK - .gitignore cree
) else (
    echo     OK - .gitignore existe deja
)

echo.
echo [3/7] Initialisation Git dans /dashboard/...
if not exist .git (
    git init
    echo     OK - Git initialise
) else (
    echo     OK - Git deja initialise
)

echo.
echo [4/7] Configuration Git...
git config user.name "Jean-Baptiste Quesnay" 2>nul
git config user.email "jbquesnay@gmail.com" 2>nul
echo     OK - Configuration Git

echo.
echo [5/7] Ajout des fichiers...
git add dashboard.py config.yaml requirements.txt .gitignore README.md
git add DASHBOARD_README.md DEPLOIEMENT_STREAMLIT_CLOUD.md
echo     OK - Fichiers ajoutes

echo.
echo [6/7] Commit initial...
git commit -m "Initial commit: Dashboard Streamlit ROYCE ROLLS XAUUSD"
if errorlevel 1 (
    echo     INFO - Aucun changement a commiter (deja fait)
) else (
    echo     OK - Commit effectue
)

echo.
echo [7/7] Verification finale...
git status
echo.

echo ========================================
echo PREPARATION TERMINEE !
echo ========================================
echo.
echo ========================================
echo PROCHAINES ETAPES MANUELLES:
echo ========================================
echo.
echo ETAPE 1: CREER UN REPO GITHUB
echo ----------------------------------------
echo 1. Ouvrir: https://github.com/new
echo 2. Repository name: royce-rolls-dashboard
echo 3. Description: Dashboard Trading XAUUSD
echo 4. Public (requis pour Streamlit gratuit)
echo 5. NE PAS cocher "Add README" ou "Add .gitignore"
echo 6. Cliquer "Create repository"
echo.
echo ETAPE 2: LIER ET PUSHER LE REPO
echo ----------------------------------------
echo Copier-coller ces commandes (remplacer VOTRE_USERNAME):
echo.
echo git remote add origin https://github.com/VOTRE_USERNAME/royce-rolls-dashboard.git
echo git branch -M main
echo git push -u origin main
echo.
echo ETAPE 3: DEPLOYER SUR STREAMLIT CLOUD
echo ----------------------------------------
echo 1. Aller sur: https://share.streamlit.io
echo 2. Se connecter avec GitHub
echo 3. Cliquer "New app" (en haut a droite)
echo 4. Selectionner:
echo    - Repository: VOTRE_USERNAME/royce-rolls-dashboard
echo    - Branch: main
echo    - Main file path: dashboard.py
echo    - App URL: royce-rolls-dashboard (personnalisable)
echo 5. Cliquer "Deploy!"
echo.
echo ETAPE 4: ATTENDRE LE DEPLOIEMENT
echo ----------------------------------------
echo Le deploiement prend 1-2 minutes
echo Vous verrez "Your app is live!" quand c'est pret
echo.
echo ETAPE 5: ACCEDER A VOTRE DASHBOARD
echo ----------------------------------------
echo URL: https://VOTRE_USERNAME-royce-rolls-dashboard.streamlit.app
echo.
echo Exemple:
echo https://jbquesnay-royce-rolls-dashboard.streamlit.app
echo.
echo ========================================
echo NOTES IMPORTANTES:
echo ========================================
echo.
echo - Le repo GitHub DOIT etre PUBLIC (gratuit)
echo - Les donnees trade_history.json ne sont PAS uploadees
echo - HTTPS securise automatique
echo - Accessible 24/7 depuis n'importe ou
echo - Mise a jour auto quand vous pushez sur GitHub
echo.
echo IDENTIFIANTS DASHBOARD:
echo   Email: jbquesnay@gmail.com
echo   Mot de passe: admin123
echo.
echo ========================================
echo SUPPORT:
echo ========================================
echo.
echo Documentation complete: DEPLOIEMENT_STREAMLIT_CLOUD.md
echo Support Streamlit: https://discuss.streamlit.io
echo.
echo ========================================

pause

