# 🌐 DÉPLOIEMENT STREAMLIT CLOUD

## Guide Complet pour Mettre le Dashboard en Ligne

---

## 🎯 **ÉTAPE 1 : PRÉPARATION DES FICHIERS**

### Structure requise
```
mt5/
├── dashboard.py              ✅ Déjà créé
├── config.yaml               ✅ Déjà créé
├── requirements.txt          ✅ Déjà créé
├── .gitignore               ⚠️ À créer
└── README.md                📝 Optionnel
```

### Créer `.gitignore`
```
# Fichiers à NE PAS mettre en ligne
trade_history.json
cumulative_data.json
session_data.json
*.pkl
*.pyc
__pycache__/
.env
.venv/
venv/
```

**⚠️ IMPORTANT** : Ne jamais mettre `trade_history.json` en ligne pour protéger vos données de trading !

---

## 🚀 **ÉTAPE 2 : CRÉER UN COMPTE STREAMLIT CLOUD**

### 1. Aller sur Streamlit Cloud
```
🌐 https://share.streamlit.io
```

### 2. S'inscrire avec GitHub
```
✅ Cliquer sur "Sign up with GitHub"
✅ Autoriser Streamlit à accéder à votre GitHub
✅ Compte créé automatiquement (100% gratuit)
```

**Limites Gratuites** :
- ✅ Illimité : Apps publiques
- ✅ 1 Go RAM par app
- ✅ 1 CPU partagé
- ✅ Aucune limite de visiteurs

---

## 📦 **ÉTAPE 3 : CRÉER UN REPO GITHUB**

### Option A : Via l'interface GitHub

1. **Aller sur GitHub** : https://github.com
2. **Cliquer sur** : `New repository` (bouton vert)
3. **Remplir** :
   ```
   Repository name: royce-rolls-dashboard
   Description: Trading Dashboard XAUUSD
   Public ✅ (requis pour Streamlit Cloud gratuit)
   Add .gitignore: Python
   ```
4. **Cliquer sur** : `Create repository`

### Option B : Via Git en ligne de commande

```bash
# Initialiser Git dans le dossier mt5
cd C:\Users\jbquesnay\Desktop\MT5-TRADINGBOT\mt5
git init

# Ajouter les fichiers
git add dashboard.py config.yaml requirements.txt .gitignore

# Premier commit
git commit -m "Initial commit: Dashboard Streamlit"

# Lier au repo GitHub
git remote add origin https://github.com/VOTRE_USERNAME/royce-rolls-dashboard.git

# Pousser vers GitHub
git push -u origin main
```

**⚠️ Remplacer** `VOTRE_USERNAME` par votre nom d'utilisateur GitHub

---

## 🌐 **ÉTAPE 4 : DÉPLOYER SUR STREAMLIT CLOUD**

### 1. Accéder au Dashboard Streamlit
```
🌐 https://share.streamlit.io
✅ Se connecter avec GitHub
```

### 2. Cliquer sur "New app"
```
📍 Bouton en haut à droite
```

### 3. Configurer l'App

**Repository** :
```
VOTRE_USERNAME/royce-rolls-dashboard
```

**Branch** :
```
main (ou master)
```

**Main file path** :
```
dashboard.py
```

**App URL (personnalisable)** :
```
royce-rolls-dashboard.streamlit.app
ou
jbquesnay-trading-dashboard.streamlit.app
```

### 4. Advanced settings (Optionnel)

Cliquer sur "Advanced settings" pour :

**Python version** :
```
3.9 (recommandé)
```

**Secrets** (pour config.yaml sensible) :
```toml
# Si vous voulez cacher config.yaml
[credentials.usernames.admin]
email = "jbquesnay@gmail.com"
name = "Jean-Baptiste Quesnay"
password = "$2b$12$KIXxPzQF7Jq3Z8.NZX9kzeYmVw7HQF5Kx3f9YQC.RqXm8Fz9XQW0O"

[cookie]
name = "royce_rolls_dashboard"
key = "royce_rolls_secret_key_2024_secure_random_string"
expiry_days = 30
```

### 5. Cliquer sur "Deploy!"
```
⏳ Déploiement en cours (1-2 minutes)
✅ App en ligne !
```

---

## 🔗 **ÉTAPE 5 : ACCÉDER À VOTRE DASHBOARD**

### URL de votre Dashboard
```
🌐 https://VOTRE_APP.streamlit.app
```

**Exemple** :
```
https://royce-rolls-dashboard.streamlit.app
https://jbquesnay-trading.streamlit.app
```

### Partager le Lien
```
✅ Accessible depuis n'importe où
✅ Mobile, Tablette, Desktop
✅ Aucune installation requise
```

---

## 📊 **ÉTAPE 6 : UPLOADER LES DONNÉES**

### Problème : trade_history.json n'est pas en ligne

**Solution 1 : Upload Manuel via l'Interface**
```
1. Se connecter au dashboard en ligne
2. Aller dans "📁 Charger Données"
3. Tab "📤 Manuel"
4. Upload trade_history.json depuis votre PC
```

**Solution 2 : Synchronisation Automatique (Avancé)**

Utiliser Streamlit Secrets + Google Drive API ou Dropbox API pour synchroniser automatiquement.

**Solution 3 : Base de Données Cloud**

Utiliser une base de données cloud gratuite :
- **Supabase** (PostgreSQL gratuit)
- **MongoDB Atlas** (NoSQL gratuit)
- **Firebase** (Google, gratuit)

---

## 🔒 **SÉCURITÉ EN LIGNE**

### 1. Protéger config.yaml

**Utiliser Streamlit Secrets** :

Dans le dashboard Streamlit Cloud :
```
Settings → Secrets → Add new secret
```

Copier le contenu de `config.yaml` :
```toml
[credentials.usernames.admin]
email = "jbquesnay@gmail.com"
name = "Jean-Baptiste Quesnay"
password = "$2b$12$..."

[credentials.usernames.jbquesnay]
email = "jbquesnay@gmail.com"
name = "Jean-Baptiste Quesnay"
password = "$2b$12$..."

[cookie]
name = "royce_rolls_dashboard"
key = "royce_rolls_secret_key_2024"
expiry_days = 30

[preauthorized.emails]
emails = ["jbquesnay@gmail.com"]
```

**Modifier dashboard.py** :
```python
# Avant
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Après
try:
    # Essayer de charger depuis Streamlit Secrets
    config = st.secrets.to_dict()
except:
    # Fallback sur config.yaml local
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
```

### 2. HTTPS Automatique
```
✅ Streamlit Cloud utilise HTTPS automatiquement
✅ Connexion sécurisée garantie
```

### 3. Authentification Obligatoire
```
✅ Déjà implémentée avec streamlit-authenticator
✅ Aucun accès sans login
```

---

## 🔄 **MISES À JOUR AUTOMATIQUES**

### Workflow Git → Streamlit

```
1. Modifier dashboard.py localement
   ↓
2. Commit et Push vers GitHub
   git add dashboard.py
   git commit -m "Update: nouvelle feature"
   git push
   ↓
3. Streamlit Cloud détecte le changement
   ↓
4. Redéploiement automatique (30 secondes)
   ↓
5. Dashboard en ligne mis à jour ✅
```

**⏱️ Temps de mise à jour** : ~30 secondes

---

## 📱 **ACCÈS DEPUIS MOBILE**

### iOS (iPhone/iPad)

1. **Safari** : Ouvrir `https://votre-app.streamlit.app`
2. **Ajouter à l'écran d'accueil** :
   ```
   Partager (⬆️) → Ajouter à l'écran d'accueil
   ```
3. **Icône créée** : Dashboard accessible comme une app native

### Android

1. **Chrome** : Ouvrir `https://votre-app.streamlit.app`
2. **Ajouter à l'écran d'accueil** :
   ```
   Menu (⋮) → Ajouter à l'écran d'accueil
   ```
3. **Icône créée** : Dashboard accessible comme une app native

---

## 🎨 **PERSONNALISATION URL**

### URL par Défaut
```
https://GITHUB_USERNAME-REPO_NAME-HASH.streamlit.app
```

### URL Personnalisée (Compte Pro)
```
https://votre-domaine.com
```

**Gratuit** :
- ✅ Sous-domaine Streamlit : `votre-app.streamlit.app`

**Payant** (Streamlit Teams - $250/mois) :
- ✅ Domaine personnalisé : `dashboard.votresite.com`
- ✅ Apps privées (pas besoin de repo public)
- ✅ Plus de ressources (4 Go RAM)

---

## 🐛 **DÉPANNAGE**

### Erreur : "Module not found"

**Vérifier `requirements.txt`** :
```
streamlit>=1.28.0
streamlit-authenticator>=0.2.3
plotly>=5.17.0
pandas>=2.1.0
pyyaml>=6.0.1
```

### Erreur : "File not found: config.yaml"

**Solutions** :
1. Vérifier que `config.yaml` est dans le repo GitHub
2. Ou utiliser Streamlit Secrets (voir section Sécurité)

### App ne démarre pas

**Logs** :
```
1. Aller sur https://share.streamlit.io
2. Cliquer sur votre app
3. Cliquer sur "Manage app" → "Logs"
4. Vérifier les erreurs
```

### App lente

**Optimisations** :
```python
# Ajouter dans dashboard.py
@st.cache_data(ttl=300)  # Cache 5 minutes
def load_data():
    # ... code de chargement
    return data
```

---

## 💰 **COÛTS**

### Streamlit Cloud (Gratuit)
```
✅ Apps publiques illimitées
✅ 1 Go RAM par app
✅ HTTPS automatique
✅ Domaine streamlit.app
❌ Apps privées (repo doit être public)
```

### Streamlit Teams ($250/mois)
```
✅ Apps privées (repos privés)
✅ 4 Go RAM par app
✅ Domaine personnalisé
✅ Support prioritaire
✅ SSO (Single Sign-On)
```

**Recommandation** : Commencer avec le plan gratuit

---

## 📋 **CHECKLIST FINALE**

Avant de déployer :

```
☑️ dashboard.py créé et testé localement
☑️ requirements.txt à jour
☑️ config.yaml configuré
☑️ .gitignore créé (exclut trade_history.json)
☑️ Repo GitHub créé
☑️ Fichiers poussés vers GitHub
☑️ Compte Streamlit Cloud créé
☑️ App déployée
☑️ URL partagée
☑️ Test connexion mobile
```

---

## 🎯 **COMMANDES RAPIDES**

### Déploiement Initial
```bash
# 1. Créer .gitignore
echo "trade_history.json
cumulative_data.json
*.pkl
__pycache__/" > .gitignore

# 2. Initialiser Git
git init
git add dashboard.py config.yaml requirements.txt .gitignore
git commit -m "Initial: Dashboard Streamlit"

# 3. Lier GitHub
git remote add origin https://github.com/VOTRE_USERNAME/royce-rolls-dashboard.git
git push -u origin main

# 4. Aller sur https://share.streamlit.io
# 5. Cliquer "New app"
# 6. Sélectionner le repo
# 7. Deploy!
```

### Mise à Jour
```bash
# Modifier dashboard.py
# Puis :
git add dashboard.py
git commit -m "Update: amélioration X"
git push

# Streamlit Cloud redéploie automatiquement
```

---

## 🌐 **VOTRE DASHBOARD SERA ACCESSIBLE**

```
✅ Depuis n'importe où dans le monde
✅ Sur tous les appareils (Mobile/Tablette/Desktop)
✅ Avec HTTPS sécurisé
✅ 24/7 sans interruption
✅ Avec URL permanente
✅ Gratuitement !
```

**URL Exemple** :
```
https://jbquesnay-trading-dashboard.streamlit.app
```

---

## 📞 **SUPPORT**

**Streamlit Community** :
- Forum : https://discuss.streamlit.io
- Docs : https://docs.streamlit.io
- Discord : https://discord.gg/streamlit

**Tutoriels Vidéo** :
- YouTube : "Streamlit Cloud deployment"
- Documentation officielle complète

---

**PRÊT POUR LE DÉPLOIEMENT EN LIGNE !** 🚀🌐

---

## 📝 **RÉSUMÉ EN 5 ÉTAPES**

1. **Créer .gitignore** (exclure données sensibles)
2. **Push vers GitHub** (repo public)
3. **Aller sur share.streamlit.io** (créer compte)
4. **New app** → Sélectionner repo → Deploy
5. **Accéder** à `https://votre-app.streamlit.app` ✅

