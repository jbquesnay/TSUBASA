# 📊 ROYCE ROLLS | Dashboard Trading

Dashboard interactif en ligne pour visualiser les performances du bot de trading XAUUSD.

🌐 **[Accéder au Dashboard en Ligne](https://share.streamlit.io)** *(à configurer)*

---

## 🚀 Déploiement Rapide (5 minutes)

### Option 1 : Script Automatique

```bash
cd dashboard
deploy_streamlit.bat
```

### Option 2 : Manuel

```bash
# 1. Créer un repo GitHub
# Aller sur https://github.com/new
# Nom: royce-rolls-dashboard
# Public ✅

# 2. Push vers GitHub
cd dashboard
git init
git add .
git commit -m "Initial: Dashboard Streamlit"
git remote add origin https://github.com/VOTRE_USERNAME/royce-rolls-dashboard.git
git branch -M main
git push -u origin main

# 3. Déployer sur Streamlit Cloud
# Aller sur https://share.streamlit.io
# New app → Sélectionner le repo → Deploy!
```

---

## 📁 Structure du Projet

```
dashboard/
├── dashboard.py                    # Application Streamlit principale
├── config.yaml                     # Configuration authentification
├── requirements.txt                # Dépendances Python
├── .gitignore                      # Fichiers à ignorer
├── README.md                       # Ce fichier
├── DASHBOARD_README.md             # Documentation complète
├── DEPLOIEMENT_STREAMLIT_CLOUD.md  # Guide déploiement détaillé
└── deploy_streamlit.bat            # Script automatique
```

---

## 💻 Installation Locale

### Prérequis
```bash
Python 3.9+
pip
```

### Installation
```bash
cd dashboard
pip install -r requirements.txt
```

### Lancement
```bash
streamlit run dashboard.py
```

**Accès** : http://localhost:8501

---

## 🔐 Identifiants

**Par défaut** :
```
Email: jbquesnay@gmail.com
Mot de passe: admin123
```

**Alternative** :
```
Username: jbquesnay
Mot de passe: 2ZZ9j$zp
```

---

## 🎯 Fonctionnalités

### 📊 Dashboard Principal
- Métriques temps réel (PNL, Trades, Win Rate)
- Graphique PnL cumulatif interactif
- Tableau des derniers trades
- Filtres de période (Jour/Semaine/Mois/Année)

### 📁 Chargement Données
- **Automatique** : Depuis `trade_history.json` du bot
- **Manuel** : Upload de fichiers JSON

### 🗑️ Gestion Sessions
- Visualisation de toutes les sessions
- Suppression sélective
- Recalcul automatique des statistiques

---

## 🌐 Déploiement en Ligne

### Streamlit Cloud (Gratuit)

**Avantages** :
- ✅ 100% Gratuit
- ✅ HTTPS automatique
- ✅ Accessible 24/7
- ✅ URL personnalisable
- ✅ Mise à jour automatique (Git)

**Limitations** :
- Repo GitHub doit être public
- 1 Go RAM par app

### Guide Complet
Voir `DEPLOIEMENT_STREAMLIT_CLOUD.md` pour le guide détaillé.

---

## 📱 Responsive Design

Optimisé pour :
- 💻 Desktop (Chrome, Firefox, Safari, Edge)
- 📱 Mobile (iOS Safari, Android Chrome)
- 🖥️ Tablette (iPad, Android)

---

## 🔄 Synchronisation avec le Bot

### Workflow

```
Bot Trading (seg_combo_working.py)
  ↓
Enregistre → trade_history.json
  ↓
Dashboard lit les données
  ↓
Affichage temps réel
```

### Actualisation

**En ligne** : Cliquer sur "🔄 Actualiser depuis le Bot"  
**Local** : Upload manuel de `trade_history.json`

---

## 🛠️ Configuration Avancée

### Changer le Mot de Passe

```python
import streamlit_authenticator as stauth

# Générer un hash
hashed = stauth.Hasher(['nouveau_mdp']).generate()
print(hashed[0])

# Copier dans config.yaml
```

### Utiliser Streamlit Secrets

**Sur Streamlit Cloud** :
```
Settings → Secrets → Coller le contenu de config.yaml
```

**Modifier dashboard.py** :
```python
try:
    config = st.secrets.to_dict()
except:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
```

---

## 🐛 Dépannage

### Module non trouvé
```bash
pip install -r requirements.txt
```

### Port déjà utilisé
```bash
streamlit run dashboard.py --server.port 8502
```

### Données ne chargent pas
1. Vérifier que `trade_history.json` existe
2. Vérifier le format JSON
3. Cliquer sur "🔄 Actualiser"

---

## 📞 Support

- 📧 Email : jbquesnay@gmail.com
- 📚 Docs Streamlit : https://docs.streamlit.io
- 💬 Forum : https://discuss.streamlit.io

---

## 📝 Changelog

### Version 1.0.0 (2025-01-29)
- ✅ Dashboard initial
- ✅ Authentification sécurisée
- ✅ Chargement automatique des données
- ✅ Graphiques interactifs Plotly
- ✅ Design responsive
- ✅ Déploiement Streamlit Cloud

---

## 📄 Licence

Propriétaire - Jean-Baptiste Quesnay

---

**🚀 Dashboard Prêt pour le Déploiement !**

**URL (après déploiement)** : `https://votre-app.streamlit.app`

