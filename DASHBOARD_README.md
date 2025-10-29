# ROYCE ROLLS | Dashboard Trading

Dashboard interactif pour visualiser les performances du bot de trading XAUUSD.

## 📋 Prérequis

```bash
pip install streamlit
pip install streamlit-authenticator
pip install plotly
pip install pandas
pip install pyyaml
```

## 🚀 Installation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Configuration (Première utilisation)

Le fichier `config.yaml` est créé automatiquement au premier lancement avec les identifiants par défaut :

**Utilisateur 1** :
- Email: `jbquesnay@gmail.com`
- Mot de passe: `admin123`

**Utilisateur 2** :
- Email: `jbquesnay@gmail.com`
- Username: `jbquesnay`
- Mot de passe: `2ZZ9j$zp`

### 3. Lancer le Dashboard

```bash
streamlit run dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

## 📱 Accès Mobile

Pour accéder depuis votre mobile/tablette :

1. Lancer le dashboard sur votre PC
2. Trouver l'IP de votre PC (ex: `192.168.1.100`)
3. Sur votre mobile, accéder à : `http://192.168.1.100:8501`

## 🎯 Fonctionnalités

### 📊 Dashboard Principal

- **Métriques Temps Réel** :
  - PNL Total
  - Nombre total de trades
  - Win Rate
  - Profit moyen

- **Graphiques** :
  - Évolution du PNL cumulé
  - Performance journalière
  - Distribution des gains/pertes

- **Tableaux** :
  - Liste des derniers trades
  - Détails par session

### 📁 Chargement de Données

**Mode Automatique** :
- Charge automatiquement depuis `trade_history.json`
- Cliquer sur "🔄 Actualiser depuis le Bot" dans la sidebar
- Ou sur "📥 Charger les données du bot"

**Mode Manuel** :
- Import de fichiers JSON personnalisés
- Fusion avec les données existantes

### 🗑️ Suppression de Sessions

- Visualiser toutes les sessions
- Sélectionner et supprimer des sessions spécifiques
- Mise à jour automatique des statistiques

### 🔍 Filtres

- **Tout** : Toutes les données
- **Jour** : Aujourd'hui uniquement
- **Semaine** : 7 derniers jours
- **Mois** : 30 derniers jours
- **Année** : 365 derniers jours
- **Personnalisé** : Période libre

## 📂 Structure des Fichiers

```
mt5/
├── dashboard.py              # Application Streamlit
├── config.yaml               # Configuration authentification
├── trade_history.json        # Données du bot (auto-généré)
├── cumulative_data.json      # Données cumulatives (auto-généré)
└── requirements.txt          # Dépendances Python
```

## 🔒 Sécurité

### Changer le Mot de Passe

Pour générer un nouveau hash de mot de passe :

```python
import streamlit_authenticator as stauth

# Hasher le nouveau mot de passe
hashed_password = stauth.Hasher(['votre_nouveau_mot_de_passe']).generate()
print(hashed_password[0])
```

Copier le hash dans `config.yaml`.

### Changer la Clé Cookie

Pour plus de sécurité, générer une nouvelle clé aléatoire :

```bash
# Linux/Mac
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32|%{Get-Random -Minimum 0 -Maximum 256}))
```

Remplacer la valeur de `cookie.key` dans `config.yaml`.

## 🎨 Personnalisation

### Modifier les Couleurs

Dans `dashboard.py`, modifier la section CSS :

```python
st.markdown("""
<style>
    .stButton>button {
        background-color: #VOTRE_COULEUR !important;
        color: #TEXTE_COULEUR !important;
    }
</style>
""", unsafe_allow_html=True)
```

### Ajouter des Métriques

Ajouter des colonnes dans la section métriques :

```python
col5 = st.columns(1)
with col5:
    st.metric("Votre Métrique", valeur)
```

## 📊 Intégration avec le Bot

Le dashboard se synchronise automatiquement avec le bot via `trade_history.json`.

### Workflow

```
Bot Trading (seg_combo_working.py)
  ↓
  Enregistre les trades dans trade_history.json
  ↓
Dashboard (dashboard.py)
  ↓
  Lit trade_history.json
  ↓
  Affiche les statistiques en temps réel
```

### Actualisation Automatique

Pour actualiser automatiquement le dashboard :

```python
# Ajouter dans dashboard.py
import time

# Actualisation toutes les 60 secondes
if st.sidebar.checkbox("🔄 Actualisation Auto"):
    time.sleep(60)
    st.rerun()
```

## 🐛 Dépannage

### Erreur : "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

### Erreur : "config.yaml not found"

Le fichier est créé automatiquement. Si problème, créer manuellement avec le contenu fourni.

### Dashboard ne charge pas les données

1. Vérifier que `trade_history.json` existe
2. Vérifier le format JSON (valide)
3. Cliquer sur "🔄 Actualiser depuis le Bot"

### Port déjà utilisé

```bash
streamlit run dashboard.py --server.port 8502
```

## 📱 Optimisation Mobile

Le dashboard est **responsive** et optimisé pour :
- ✅ iPhone (Safari)
- ✅ iPad (Safari)
- ✅ Android (Chrome)
- ✅ Desktop (tous navigateurs)

### Tailles d'écran supportées

- Mobile : < 480px
- Tablette : 480px - 768px
- Desktop : > 768px

## 🚀 Déploiement en Production

### Option 1 : Streamlit Cloud (Gratuit)

1. Créer un compte sur [streamlit.io](https://streamlit.io)
2. Connecter votre repo GitHub
3. Déployer en 1 clic

### Option 2 : Serveur Dédié

```bash
# Installer screen pour garder le processus actif
apt-get install screen

# Lancer en arrière-plan
screen -S dashboard
streamlit run dashboard.py --server.port 8501
# Ctrl+A puis D pour détacher
```

### Option 3 : Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py"]
```

```bash
docker build -t royce-dashboard .
docker run -p 8501:8501 royce-dashboard
```

## 📞 Support

Pour toute question ou problème :
- Email : jbquesnay@gmail.com
- Documentation Streamlit : [docs.streamlit.io](https://docs.streamlit.io)

## 📝 Changelog

### Version 1.0.0 (2025-01-29)

- ✅ Dashboard initial
- ✅ Authentification sécurisée
- ✅ Chargement automatique des données
- ✅ Filtres de période
- ✅ Graphiques interactifs
- ✅ Responsive mobile
- ✅ Suppression de sessions

---

**DASHBOARD PRÊT À L'EMPLOI !** 🚀📊

