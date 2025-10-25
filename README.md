# 📊 Tsubasa Trading Dashboard

Dashboard de performance pour le bot de trading Tsubasa.

## 🚀 Déploiement sur Streamlit Cloud

Ce dashboard affiche les performances de trading en temps réel avec :
- KPI quotidiens, hebdomadaires, mensuels
- Calendriers visuels (vert/rouge par jour)
- Distribution des trades
- Analyse de confiance ML

## 📁 Fichiers

- `tsubasa_dashboard.py` : Application Streamlit principale
- `requirements_dashboard.txt` : Dépendances Python
- `trade_history.json` : Données de trading (mis à jour automatiquement)

## 🌐 Accès

Dashboard accessible à l'adresse fournie par Streamlit Cloud après déploiement.

## 🔧 Installation Locale

```bash
pip install -r requirements_dashboard.txt
streamlit run tsubasa_dashboard.py
```

## 📈 Fonctionnalités

### Vue d'Ensemble
- PnL total et journalier
- Nombre de trades
- Win rate
- Drawdown maximum

### Calendriers
- **Calendrier Hebdomadaire** : Jours en colonnes, semaines en lignes
- **Calendrier Mensuel** : Semaines complètes avec PnL cumulé

### Analyses
- Distribution des profits/pertes
- Performance par heure
- Statistiques de confiance ML
- Métriques avancées

## 🎨 Design

Dashboard minimaliste noir & blanc avec design angulaire.

## 📊 Source de Données

Les données proviennent de `trade_history.json` généré par le bot de trading.

Format des données :
```json
{
  "timestamp_open": 1234567890000,
  "timestamp_close": 1234567890000,
  "side": "BUY",
  "result": "WIN",
  "pnl": 245.50,
  "confidence_init": 45.0,
  "confidence_final": 48.0,
  ...
}
```

## 🔄 Mise à Jour

Les données sont mises à jour automatiquement :
- Le bot génère `trade_history.json`
- Commit et push sur GitHub
- Streamlit Cloud se met à jour automatiquement

## 📝 Notes

- Dashboard optimisé pour usage personnel
- Données historiques conservées dans `trade_history.json`
- Compatible avec orchestrator_master et orchestrator_tsubasa

---

**Version** : 1.0  
**Date** : 25 octobre 2025  
**Auteur** : Tsubasa Trading System

