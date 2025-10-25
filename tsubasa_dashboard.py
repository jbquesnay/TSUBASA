#!/usr/bin/env python3
"""
TSUBASA INVESTMENT SYSTEM – LIVE DASHBOARD
Design minimal noir & blanc, style hedge-fund
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import numpy as np
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="TSUBASA Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",  # Collapse automatiquement sur mobile
    menu_items={
        'About': "TSUBASA Trading Dashboard - Responsive Mobile & Desktop"
    }
)

# CSS personnalisé - Design minimal noir & blanc
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', 'Avenir Next LT Pro', 'Avenir', sans-serif !important;
    }
    
    /* Fond et texte */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Header */
    .main-header {
        background-color: #000000;
        color: #FFFFFF;
        padding: 24px;
        margin-bottom: 48px;
        border-radius: 0px;
    }
    
    .main-title {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .main-subtitle {
        font-size: 14px;
        font-weight: 300;
        letter-spacing: 0.5px;
        margin-top: 8px;
        opacity: 0.8;
    }
    
    /* Métriques */
    .metric-card {
        background-color: #FFFFFF;
        border: 0.5px solid #000000;
        padding: 24px;
        border-radius: 0px;
        margin-bottom: 12px;
    }
    
    .metric-label {
        font-size: 12px;
        font-weight: 400;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #666666;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 600;
        letter-spacing: -1px;
        color: #000000;
    }
    
    .metric-value.positive {
        color: #000000;
    }
    
    .metric-value.negative {
        color: #666666;
    }
    
    /* Sections */
    .section-header {
        font-size: 18px;
        font-weight: 600;
        letter-spacing: -0.3px;
        margin-top: 48px;
        margin-bottom: 24px;
        padding-bottom: 12px;
        border-bottom: 0.5px solid #000000;
    }
    
    /* Tableaux */
    .dataframe {
        border: 0.5px solid #000000 !important;
        border-radius: 0px !important;
    }
    
    .dataframe th {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 11px !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        padding: 12px !important;
        border: none !important;
    }
    
    .dataframe td {
        font-size: 13px !important;
        font-weight: 400 !important;
        padding: 12px !important;
        border: 0.5px solid #E0E0E0 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #F5F5F5;
        border-right: 0.5px solid #000000;
    }
    
    /* Boutons */
    .stButton > button {
        background-color: #000000;
        color: #FFFFFF;
        border: none;
        border-radius: 0px;
        padding: 12px 24px;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-size: 11px;
    }
    
    .stButton > button:hover {
        background-color: #333333;
    }
    
    /* Graphiques Plotly */
    .js-plotly-plot {
        border: 0.5px solid #E0E0E0;
        border-radius: 0px;
    }
    
    /* ============================================
       RESPONSIVE MOBILE (iPhone et autres)
       ============================================ */
    
    @media only screen and (max-width: 768px) {
        /* Header plus compact */
        .main-header {
            padding: 16px;
            margin-bottom: 24px;
        }
        
        .main-title {
            font-size: 24px;
            letter-spacing: -0.3px;
        }
        
        .main-subtitle {
            font-size: 12px;
        }
        
        /* Métriques adaptées */
        .metric-card {
            padding: 16px;
            margin-bottom: 8px;
        }
        
        .metric-label {
            font-size: 10px;
            margin-bottom: 6px;
        }
        
        .metric-value {
            font-size: 28px;
            letter-spacing: -0.5px;
        }
        
        /* Sections plus compactes */
        .section-header {
            font-size: 16px;
            margin-top: 32px;
            margin-bottom: 16px;
            padding-bottom: 8px;
        }
        
        /* Tableaux responsive */
        .dataframe th {
            font-size: 9px !important;
            padding: 8px !important;
        }
        
        .dataframe td {
            font-size: 11px !important;
            padding: 8px !important;
        }
        
        /* Boutons adaptés */
        .stButton > button {
            padding: 10px 16px;
            font-size: 10px;
            width: 100%;
        }
        
        /* Colonnes Streamlit en mode stack sur mobile */
        .row-widget.stHorizontal {
            flex-direction: column !important;
        }
        
        /* Sidebar en overlay sur mobile */
        [data-testid="stSidebar"] {
            width: 280px !important;
        }
        
        /* Padding général réduit */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
        }
        
        /* Graphiques full-width sur mobile */
        .js-plotly-plot {
            width: 100% !important;
            height: auto !important;
        }
    }
    
    /* iPhone spécifique (petits écrans) */
    @media only screen and (max-width: 430px) {
        .main-title {
            font-size: 20px;
        }
        
        .metric-value {
            font-size: 24px;
        }
        
        .section-header {
            font-size: 14px;
        }
        
        /* Tableaux encore plus compacts */
        .dataframe th {
            font-size: 8px !important;
            padding: 6px !important;
        }
        
        .dataframe td {
            font-size: 10px !important;
            padding: 6px !important;
        }
    }
    
    /* Mode paysage mobile */
    @media only screen and (max-width: 768px) and (orientation: landscape) {
        .main-header {
            padding: 12px;
            margin-bottom: 16px;
        }
        
        .metric-card {
            padding: 12px;
        }
    }
    
    /* Touch-friendly sur mobile */
    @media (hover: none) and (pointer: coarse) {
        .stButton > button {
            min-height: 44px;
        }
        
        .metric-card {
            margin-bottom: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)


class TsubasaDashboard:
    """Dashboard principal Tsubasa"""
    
    def __init__(self, json_path="trade_history.json"):
        self.json_path = json_path
    
    def get_responsive_config(self):
        """Configuration responsive pour les graphiques Plotly"""
        return {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'responsive': True,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'tsubasa_chart',
                'height': 500,
                'width': 1200,
                'scale': 2
            }
        }
    
    def get_responsive_layout(self, base_height=300):
        """Layout responsive qui s'adapte à la taille de l'écran"""
        # Sur mobile, les graphiques seront plus hauts pour compenser la largeur réduite
        return {
            'height': base_height,
            'autosize': True,
            'margin': dict(l=40, r=20, t=40, b=40)
        }
        
    def load_trades(self, start_date=None, end_date=None):
        """Charge les trades depuis trade_history.json (données réelles de royce_rolls.bat)"""
        
        # Vérifier si le fichier existe
        if not Path(self.json_path).exists():
            st.warning(f"⚠️ Fichier de trades non trouvé : {self.json_path}")
            st.info("💡 Lancez **royce_rolls.bat** pour générer des données de trading")
            return pd.DataFrame()
        
        try:
            # Charger le JSON
            with open(self.json_path, 'r', encoding='utf-8') as f:
                trades = json.load(f)
            
            if not trades:
                st.warning("⚠️ Aucun trade trouvé dans trade_history.json")
                return pd.DataFrame()
            
            # Filtrer les trades fermés uniquement
            closed_trades = [t for t in trades if t.get('result') is not None and t.get('timestamp_close') is not None]
            
            if not closed_trades:
                st.warning("⚠️ Aucun trade fermé trouvé")
                st.info("Les trades s'afficheront une fois fermés par le bot")
                return pd.DataFrame()
            
            # Convertir en DataFrame
            df = pd.DataFrame(closed_trades)
            
            # Convertir les timestamps ISO en timestamps epoch (millisecondes)
            df['ts_open'] = pd.to_datetime(df['timestamp_open']).astype(int) // 10**6
            df['ts_close'] = pd.to_datetime(df['timestamp_close']).astype(int) // 10**6
            
            # Dates
            df['date_open'] = pd.to_datetime(df['timestamp_open'])
            df['date_close'] = pd.to_datetime(df['timestamp_close'])
            df['date'] = df['date_open'].dt.date
            
            # Renommer/créer les colonnes pour correspondre au format attendu
            if 'confidence' in df.columns:
                df['confidence_final'] = df['confidence']
            
            if 'confidence_initial' in df.columns:
                df['confidence_init'] = df['confidence_initial']
            elif 'confidence' in df.columns:
                df['confidence_init'] = df['confidence']
            
            if 'profit' in df.columns:
                df['pnl_eur'] = df['profit']
            
            # Colonnes supplémentaires avec valeurs par défaut
            if 'worker' not in df.columns:
                df['worker'] = 'orchestrator'
            
            if 'symbol' not in df.columns:
                df['symbol'] = 'XAUUSD'
            
            if 'side' not in df.columns:
                df['side'] = df['direction'] if 'direction' in df.columns else 'BUY'
            
            if 'lots' not in df.columns:
                df['lots'] = 2.0
            
            if 'spread_pts' not in df.columns:
                df['spread_pts'] = df['spread'] if 'spread' in df.columns else 0
            
            # ML probability
            if 'ml_prob' not in df.columns:
                df['ml_prob'] = 0.5
            
            # Durée
            if 'duration' in df.columns:
                df['duration_s'] = df['duration']
            else:
                df['duration_s'] = (df['ts_close'] - df['ts_open']) / 1000
            
            # Filtrer par date si fourni
            if start_date:
                df = df[df['date'] >= start_date]
            
            if end_date:
                df = df[df['date'] <= end_date]
            
            # Trier par date décroissante
            df = df.sort_values('ts_open', ascending=False)
            
            return df
        
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement des données : {e}")
            st.error(f"Détails : {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return pd.DataFrame()
            
    def calculate_daily_stats(self, df):
        """Calcule les stats journalières"""
        if df.empty:
            return pd.DataFrame()
            
        daily = df.groupby('date').agg({
            'trade_id': 'count',
            'pnl_eur': ['sum', 'mean', 'min', 'max', 'std'],
            'result': lambda x: (x == 'WIN').sum(),
            'confidence_init': 'mean',
            'ml_prob': 'mean',
            'adx_m5': 'mean',
            'atr_m1': 'mean',
            'duration_s': 'mean'
        }).reset_index()
        
        daily.columns = ['date', 'trades', 'pnl', 'avg_pnl', 'worst_trade', 'best_trade', 
                        'pnl_std', 'wins', 'avg_conf', 'avg_ml', 'avg_adx', 'avg_atr', 'avg_duration']
        
        daily['losses'] = daily['trades'] - daily['wins']
        daily['winrate'] = (daily['wins'] / daily['trades'] * 100).round(2)
        
        return daily
        
    def plot_pnl_curve(self, df, title="PnL Cumulatif"):
        """Graphique PnL cumulatif"""
        if df.empty:
            return None
            
        df_sorted = df.sort_values('ts_open')
        df_sorted['pnl_cumul'] = df_sorted['pnl_eur'].cumsum()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_sorted['date_open'],
            y=df_sorted['pnl_cumul'],
            mode='lines',
            line=dict(color='black', width=1),
            fill='tozeroy',
            fillcolor='rgba(0,0,0,0.05)',
            name='PnL'
        ))
        
        responsive_layout = self.get_responsive_layout(base_height=300)
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, weight=600)),
            xaxis_title="",
            yaxis_title="PnL (€)",
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11),
            **responsive_layout
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#E0E0E0',
            showline=True,
            linewidth=0.5,
            linecolor='black'
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#E0E0E0',
            showline=True,
            linewidth=0.5,
            linecolor='black',
            zeroline=True,
            zerolinewidth=0.5,
            zerolinecolor='black'
        )
        
        return fig
        
    def plot_winrate_bar(self, daily_df, title="WinRate Journalier"):
        """Graphique en barres du WinRate"""
        if daily_df.empty:
            return None
            
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=daily_df['date'],
            y=daily_df['winrate'],
            marker=dict(
                color=daily_df['winrate'],
                colorscale=[[0, '#CCCCCC'], [0.5, '#999999'], [1, '#000000']],
                showscale=False,
                line=dict(color='black', width=0.5)
            ),
            name='WinRate'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, weight=600)),
            xaxis_title="",
            yaxis_title="WinRate (%)",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11),
            margin=dict(l=60, r=20, t=40, b=40),
            height=300
        )
        
        fig.update_xaxes(showgrid=False, showline=True, linewidth=0.5, linecolor='black')
        fig.update_yaxes(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#E0E0E0',
            showline=True,
            linewidth=0.5,
            linecolor='black',
            range=[0, 100]
        )
        
        return fig
        
    def plot_scatter_confidence_pnl(self, df, title="Confidence vs PnL"):
        """Scatter Confidence vs PnL"""
        if df.empty:
            return None
            
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['confidence_final'],
            y=df['pnl_eur'],
            mode='markers',
            marker=dict(
                size=6,
                color=df['pnl_eur'],
                colorscale=[[0, '#CCCCCC'], [0.5, '#FFFFFF'], [1, '#000000']],
                showscale=False,
                line=dict(color='black', width=0.5),
                opacity=0.6
            ),
            text=df['trade_id'],
            hovertemplate='Conf: %{x:.1f}%<br>PnL: %{y:.2f}€<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, weight=600)),
            xaxis_title="Confidence (%)",
            yaxis_title="PnL (€)",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11),
            margin=dict(l=60, r=20, t=40, b=40),
            height=300
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='#E0E0E0')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='#E0E0E0', zeroline=True)
        
        return fig
    
    def plot_weekly_calendar(self, df, title="Calendrier Hebdomadaire"):
        """Calendrier hebdomadaire avec jours verts/rouges"""
        if df.empty:
            return None
        
        # Préparer les données par jour
        df['date'] = pd.to_datetime(df['ts_close'], unit='ms').dt.date
        daily_pnl = df.groupby('date')['pnl_eur'].sum().reset_index()
        daily_pnl['date'] = pd.to_datetime(daily_pnl['date'])
        daily_pnl['week'] = daily_pnl['date'].dt.isocalendar().week
        daily_pnl['weekday'] = daily_pnl['date'].dt.dayofweek  # 0=Lundi, 6=Dimanche
        daily_pnl['weekday_name'] = daily_pnl['date'].dt.strftime('%a')  # Lun, Mar, etc.
        
        # Pivoter pour avoir semaines x jours
        pivot_data = daily_pnl.pivot_table(
            values='pnl_eur',
            index='week',
            columns='weekday',
            aggfunc='sum',
            fill_value=0
        )
        
        # Noms des jours (Lun-Dim)
        day_names = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        
        # Créer la heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=day_names,
            y=[f"S{w}" for w in pivot_data.index],
            colorscale=[
                [0, '#FF4444'],      # Rouge pour pertes
                [0.5, '#FFFFFF'],    # Blanc pour zéro
                [1, '#00CC00']       # Vert pour gains
            ],
            zmid=0,
            text=pivot_data.values,
            texttemplate='%{text:.0f}€',
            textfont={"size": 10, "family": "Inter, sans-serif", "color": "black"},
            hovertemplate='%{y} - %{x}<br>PnL: %{z:.2f}€<extra></extra>',
            showscale=False,
            xgap=2,
            ygap=2
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=14, weight=600)),
            xaxis_title="",
            yaxis_title="Semaine",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11),
            margin=dict(l=60, r=20, t=40, b=40),
            height=400,
            xaxis=dict(side='top')
        )
        
        return fig
    
    def plot_monthly_calendar(self, df, title="Calendrier Mensuel - Cumul par Semaine"):
        """Calendrier mensuel avec PnL total par semaine (une barre par semaine)"""
        if df.empty:
            return None
        
        # Préparer les données par jour
        df['date'] = pd.to_datetime(df['ts_close'], unit='ms').dt.date
        daily_pnl = df.groupby('date')['pnl_eur'].sum().reset_index()
        daily_pnl['date'] = pd.to_datetime(daily_pnl['date'])
        
        # Obtenir le mois actuel ou le plus récent
        latest_date = daily_pnl['date'].max()
        year = latest_date.year
        month = latest_date.month
        
        # Filtrer pour le mois
        month_data = daily_pnl[
            (daily_pnl['date'].dt.year == year) & 
            (daily_pnl['date'].dt.month == month)
        ].copy()
        
        # Calculer la semaine du mois (0-5)
        import calendar
        first_day = pd.Timestamp(year, month, 1)
        month_data['week_of_month'] = (
            (month_data['date'].dt.day + first_day.dayofweek - 1) // 7
        )
        
        # Calculer le PnL TOTAL par semaine (cumul de tous les jours)
        week_totals = month_data.groupby('week_of_month')['pnl_eur'].sum().reset_index()
        week_totals.columns = ['week', 'pnl_total']
        
        # Compter le nombre de trades par semaine
        df['date'] = pd.to_datetime(df['ts_close'], unit='ms').dt.date
        df['date'] = pd.to_datetime(df['date'])
        month_trades = df[
            (df['date'].dt.year == year) & 
            (df['date'].dt.month == month)
        ].copy()
        month_trades['week_of_month'] = (
            (month_trades['date'].dt.day + first_day.dayofweek - 1) // 7
        )
        trade_counts = month_trades.groupby('week_of_month').size().reset_index(name='nb_trades')
        
        # Fusionner
        week_data = week_totals.merge(trade_counts, left_on='week', right_on='week_of_month', how='left')
        week_data['nb_trades'] = week_data['nb_trades'].fillna(0).astype(int)
        
        # Créer une grille simple : 1 ligne × N semaines
        max_weeks = int(week_data['week'].max()) + 1
        pnl_grid = np.full((1, max_weeks), np.nan)
        text_grid = [[]]
        
        for _, row in week_data.iterrows():
            week = int(row['week'])
            pnl = row['pnl_total']
            nb = int(row['nb_trades'])
            if week < max_weeks:
                pnl_grid[0, week] = pnl
                text_grid[0].append(f"{pnl:+.0f}€<br>({nb} trades)")
        
        # Compléter avec des cellules vides si nécessaire
        while len(text_grid[0]) < max_weeks:
            text_grid[0].append("")
        
        # Labels des semaines avec dates
        x_labels = []
        for week in range(max_weeks):
            week_data_filtered = month_data[month_data['week_of_month'] == week]
            if not week_data_filtered.empty:
                first_date = week_data_filtered['date'].min().strftime('%d/%m')
                last_date = week_data_filtered['date'].max().strftime('%d/%m')
                x_labels.append(f"S{week+1}<br>{first_date}-{last_date}")
            else:
                x_labels.append(f"S{week+1}")
        
        # Créer la heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pnl_grid,
            x=x_labels,
            y=['Total Semaine'],
            colorscale=[
                [0, '#FF4444'],      # Rouge pour pertes
                [0.5, '#FFFFFF'],    # Blanc pour zéro
                [1, '#00CC00']       # Vert pour gains
            ],
            zmid=0,
            text=text_grid,
            texttemplate='%{text}',
            textfont={"size": 14, "family": "Inter, sans-serif", "color": "black", "weight": "bold"},
            hovertemplate='%{x}<br>PnL Total: %{z:.2f}€<extra></extra>',
            showscale=False,
            xgap=4,
            ygap=0
        ))
        
        month_name = latest_date.strftime('%B %Y')
        
        # Calculer le total du mois
        month_total = week_totals['pnl_total'].sum()
        nb_trades_total = trade_counts['nb_trades'].sum()
        
        fig.update_layout(
            title=dict(
                text=f"{title} - {month_name}<br><sub>Total Mois: {month_total:+.2f}€ • {nb_trades_total} trades</sub>",
                font=dict(size=14, weight=600)
            ),
            xaxis_title="",
            yaxis_title="",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=11),
            margin=dict(l=120, r=20, t=70, b=80),
            height=200,
            xaxis=dict(side='top'),
            yaxis=dict(showticklabels=False)
        )
        
        return fig


def main():
    """Fonction principale du dashboard"""
    
    # Initialiser le dashboard
    dashboard = TsubasaDashboard()
    
    # === HEADER ===
    st.markdown("""
    <div class="main-header">
        <div class="main-title">TSUBASA INVESTMENT SYSTEM – LIVE DASHBOARD</div>
        <div class="main-subtitle">Session 8h Only • XAUUSD • Royce Rolls</div>
    </div>
    """, unsafe_allow_html=True)
    
    # === SIDEBAR - FILTRES ===
    with st.sidebar:
        st.markdown("### ⚙️ Filtres & Options")
        
        # Période
        period = st.selectbox(
            "📆 Période",
            ["Aujourd'hui", "Cette semaine", "Ce mois", "Tout l'historique", "Personnalisé"]
        )
        
        # Auto-refresh
        auto_refresh = st.checkbox("🔄 Auto-refresh (2s)", value=False)
        
        if auto_refresh:
            st.empty()
            import time
            time.sleep(2)
            st.rerun()
        
        # Export
        st.markdown("---")
        st.markdown("### 💾 Export")
        if st.button("📥 Export CSV"):
            st.info("Export en cours...")
        
        if st.button("📸 Export PNG"):
            st.info("Snapshot en cours...")
    
    # Calculer les dates selon la période
    today = datetime.now().date()
    
    if period == "Aujourd'hui":
        start_date = today
        end_date = today
    elif period == "Cette semaine":
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif period == "Ce mois":
        start_date = today.replace(day=1)
        end_date = today
    elif period == "Personnalisé":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Date début", today - timedelta(days=30))
        with col2:
            end_date = st.date_input("Date fin", today)
    else:  # Tout l'historique
        start_date = None
        end_date = None
    
    # Charger les données
    df_trades = dashboard.load_trades(start_date, end_date)
    
    if df_trades.empty:
        st.warning("⚠️ Aucune donnée disponible pour la période sélectionnée")
        return
    
    # Calculer les stats
    daily_stats = dashboard.calculate_daily_stats(df_trades)
    
    # === 1️⃣ SECTION - RÉSUMÉ PRINCIPAL ===
    st.markdown('<div class="section-header">📊 Résumé de la Période</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_pnl = df_trades['pnl_eur'].sum()
        pnl_class = "positive" if total_pnl > 0 else "negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📈 PnL Total</div>
            <div class="metric-value {pnl_class}">{total_pnl:+.2f}€</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_trades = len(df_trades)
        wins = (df_trades['result'] == 'WIN').sum()
        winrate = (wins / total_trades * 100) if total_trades > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">✅ WinRate</div>
            <div class="metric-value">{winrate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_win = df_trades[df_trades['result'] == 'WIN']['pnl_eur'].mean() if wins > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Gain Moyen</div>
            <div class="metric-value">{avg_win:.2f}€</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        max_dd = df_trades['pnl_eur'].min()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📉 Max Drawdown</div>
            <div class="metric-value negative">{max_dd:.2f}€</div>
        </div>
        """, unsafe_allow_html=True)
    
    # === GRAPHIQUES PRINCIPAUX ===
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pnl = dashboard.plot_pnl_curve(df_trades, "PnL Cumulatif")
        if fig_pnl:
            st.plotly_chart(fig_pnl, use_container_width=True, config=dashboard.get_responsive_config())
    
    with col2:
        if not daily_stats.empty:
            fig_wr = dashboard.plot_winrate_bar(daily_stats, "WinRate Journalier")
            if fig_wr:
                st.plotly_chart(fig_wr, use_container_width=True, config=dashboard.get_responsive_config())
    
    # === 2️⃣ SECTION - CALENDRIERS VISUELS ===
    st.markdown('<div class="section-header">📅 Calendriers Visuels - Jours Verts/Rouges</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_weekly = dashboard.plot_weekly_calendar(df_trades, "📆 Calendrier Hebdomadaire")
        if fig_weekly:
            st.plotly_chart(fig_weekly, use_container_width=True, config=dashboard.get_responsive_config())
    
    with col2:
        fig_monthly = dashboard.plot_monthly_calendar(df_trades, "📅 Calendrier Mensuel")
        if fig_monthly:
            st.plotly_chart(fig_monthly, use_container_width=True, config=dashboard.get_responsive_config())
    
    # === 3️⃣ SECTION - STATISTIQUES DÉTAILLÉES ===
    st.markdown('<div class="section-header">📈 Statistiques Détaillées</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔢 Total Trades", total_trades)
        st.metric("✅ Wins", wins)
        st.metric("❌ Losses", total_trades - wins)
    
    with col2:
        avg_pnl = df_trades['pnl_eur'].mean()
        st.metric("💵 PnL Moyen", f"{avg_pnl:.2f}€")
        
        avg_loss = df_trades[df_trades['result'] == 'LOSS']['pnl_eur'].mean() if (total_trades - wins) > 0 else 0
        st.metric("📉 Perte Moyenne", f"{avg_loss:.2f}€")
        
        # Expectancy
        expectancy = (winrate/100 * avg_win) - ((1 - winrate/100) * abs(avg_loss))
        st.metric("🎯 Expectancy", f"{expectancy:.2f}€")
    
    with col3:
        avg_conf = df_trades['confidence_final'].mean()
        st.metric("🧠 Confidence Moy.", f"{avg_conf:.1f}%")
        
        avg_ml = df_trades['ml_prob'].mean() * 100 if df_trades['ml_prob'].notna().any() else 0
        st.metric("🤖 ML Prob. Moy.", f"{avg_ml:.1f}%")
        
        avg_duration = df_trades['duration_s'].mean() / 60
        st.metric("⏱️ Durée Moy.", f"{avg_duration:.1f}min")
    
    # === 3️⃣ SECTION - ANALYSE ML & INDICATEURS ===
    st.markdown('<div class="section-header">🧠 Analyse ML & Indicateurs</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = dashboard.plot_scatter_confidence_pnl(df_trades, "Confidence vs PnL")
        if fig_scatter:
            st.plotly_chart(fig_scatter, use_container_width=True, config=dashboard.get_responsive_config())
    
    with col2:
        # Stats indicateurs
        st.markdown("**📊 Indicateurs Moyens**")
        
        col_a, col_b = st.columns(2)
        with col_a:
            avg_adx = df_trades['adx_m5'].mean()
            avg_atr = df_trades['atr_m1'].mean()
            st.metric("ADX M5", f"{avg_adx:.1f}")
            st.metric("ATR M1", f"{avg_atr:.2f}")
        
        with col_b:
            avg_rsi = df_trades['rsi_m1'].mean()
            avg_spread = df_trades['spread_pts'].mean()
            st.metric("RSI M1", f"{avg_rsi:.1f}")
            st.metric("Spread", f"{avg_spread:.1f}pts")
    
    # === 4️⃣ SECTION - TABLEAU DES TRADES ===
    st.markdown('<div class="section-header">📋 Derniers Trades</div>', unsafe_allow_html=True)
    
    df_display = df_trades[['date_open', 'worker', 'side', 'pnl_eur', 'result', 
                            'confidence_final', 'ml_prob', 'duration_s']].head(20).copy()
    df_display['duration_s'] = (df_display['duration_s'] / 60).round(1)
    df_display['ml_prob'] = (df_display['ml_prob'] * 100).round(1)
    
    df_display.columns = ['Date', 'Worker', 'Side', 'PnL (€)', 'Result', 'Conf (%)', 'ML (%)', 'Durée (min)']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # === FOOTER ===
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999999; font-size: 11px; padding: 24px;">
        TSUBASA INVESTMENT SYSTEM • Dashboard v1.0 • Data from SQLite WAL
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

