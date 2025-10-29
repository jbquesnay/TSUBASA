import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration de la page ---
st.set_page_config(
    page_title="ROYCE ROLLS | DASHBOARD XAUUSD",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    body {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    
    .stMetric {
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        background-color: #FAFAFA !important;
    }
    
    .stMetric label {
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #666666 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 600 !important;
    }
    
    .stButton>button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
    
    .stButton>button:hover {
        background-color: #333333 !important;
    }
    
    @media (max-width: 768px) {
        .stMetric {
            width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Fonction pour Charger Toutes les Sessions ---
def load_all_sessions():
    """Charger toutes les sessions depuis /dashboard/"""
    all_trades = []
    sessions_info = []
    
    # Charger tous les fichiers session_*.json
    session_files = sorted(Path('.').glob('session_*.json'))
    
    for session_file in session_files:
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
                
                # Récupérer les trades de cette session
                trades = session_data.get('trades', [])
                
                # Ajouter l'ID de session à chaque trade pour traçabilité
                for trade in trades:
                    trade['session_id'] = session_data.get('session_id')
                    trade['session_date'] = session_data.get('date')
                
                all_trades.extend(trades)
                
                # ✅ RECALCULER les stats depuis les trades (pas depuis le JSON)
                # pour garantir la cohérence des données
                session_trades_pnl = sum(t.get('profit', 0) for t in trades)
                session_wins = len([t for t in trades if t.get('result') == 'WIN'])
                session_losses = len([t for t in trades if t.get('result') == 'LOSS'])
                session_total = len(trades)
                session_win_rate = (session_wins / session_total * 100) if session_total > 0 else 0
                
                # Ajouter les infos de session (recalculées)
                sessions_info.append({
                    'session_id': session_data.get('session_id'),
                    'date': session_data.get('date'),
                    'time': session_data.get('time', ''),
                    'timestamp': session_data.get('timestamp'),
                    'total_pnl': session_trades_pnl,  # ✅ Recalculé
                    'total_trades': session_total,     # ✅ Recalculé
                    'wins': session_wins,               # ✅ Recalculé
                    'losses': session_losses,           # ✅ Recalculé
                    'win_rate': session_win_rate        # ✅ Recalculé
                })
        except Exception as e:
            st.warning(f"⚠️ Erreur chargement {session_file.name}: {e}")
    
    return all_trades, sessions_info

# --- Initialisation ---
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# --- Barre Latérale ---
st.sidebar.title("📊 ROYCE ROLLS")
st.sidebar.markdown("**Trading Dashboard XAUUSD**")
st.sidebar.markdown("---")

# Bouton Actualiser
if st.sidebar.button("🔄 Actualiser"):
    st.session_state.data_loaded = False
    st.rerun()

# --- Chargement des Données ---
all_trades, sessions_info = load_all_sessions()

if not all_trades:
    st.warning("⚠️ Aucune session trouvée")
    st.info("Les fichiers session_*.json doivent être dans le même dossier que dashboard.py")
    st.stop()

# Conversion en DataFrame
df_trades = pd.DataFrame(all_trades)
df_sessions = pd.DataFrame(sessions_info)

# Convertir les timestamps avec gestion d'erreurs
if 'timestamp_close' in df_trades.columns:
    try:
        df_trades['timestamp_close'] = pd.to_datetime(df_trades['timestamp_close'], errors='coerce')
        # Supprimer les lignes avec des timestamps invalides
        df_trades = df_trades.dropna(subset=['timestamp_close'])
    except Exception as e:
        st.error(f"❌ Erreur conversion timestamp_close: {e}")
        
if 'timestamp_open' in df_trades.columns:
    try:
        df_trades['timestamp_open'] = pd.to_datetime(df_trades['timestamp_open'], errors='coerce')
    except Exception as e:
        st.warning(f"⚠️ Erreur conversion timestamp_open: {e}")

# --- Filtres ---
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtres")

time_filter = st.sidebar.radio(
    "Période",
    ["Tout", "Jour (24h)", "Semaine (7j)", "Mois (30j)", "Année (365j)", "Personnalisé"],
    horizontal=False
)

# Appliquer les filtres
df_filtered = df_trades.copy()

if not df_filtered.empty and 'timestamp_close' in df_filtered.columns:
    if time_filter == "Jour (24h)":
        # Dernier jour = dernières 24 heures
        last_24h = datetime.now() - timedelta(days=1)
        df_filtered = df_filtered[df_filtered['timestamp_close'] >= last_24h]
    elif time_filter == "Semaine (7j)":
        # 7 derniers jours
        week_ago = datetime.now() - timedelta(days=7)
        df_filtered = df_filtered[df_filtered['timestamp_close'] >= week_ago]
    elif time_filter == "Mois (30j)":
        # 30 derniers jours
        month_ago = datetime.now() - timedelta(days=30)
        df_filtered = df_filtered[df_filtered['timestamp_close'] >= month_ago]
    elif time_filter == "Année (365j)":
        # 365 derniers jours
        year_ago = datetime.now() - timedelta(days=365)
        df_filtered = df_filtered[df_filtered['timestamp_close'] >= year_ago]
    elif time_filter == "Personnalisé":
        col1, col2 = st.sidebar.columns(2)
        start_date = col1.date_input("Début", datetime.now() - timedelta(days=30))
        end_date = col2.date_input("Fin", datetime.now())
        df_filtered = df_filtered[
            (df_filtered['timestamp_close'].dt.date >= start_date) &
            (df_filtered['timestamp_close'].dt.date <= end_date)
        ]
    # Si "Tout" est sélectionné, garder df_filtered = df_trades.copy() (pas de filtre)

# --- Dashboard Principal ---
st.title("📈 ROYCE ROLLS | DASHBOARD XAUUSD")

# 🔍 DEBUG: Afficher les informations de filtrage
if len(df_filtered) == 0 and len(df_trades) > 0:
    st.warning(f"⚠️ Filtre actif: **{time_filter}** - Aucun trade trouvé pour cette période")
    
    # Afficher la période des données disponibles
    if 'timestamp_close' in df_trades.columns and not df_trades.empty:
        min_date = df_trades['timestamp_close'].min()
        max_date = df_trades['timestamp_close'].max()
        st.info(f"📅 Données disponibles du {min_date.strftime('%Y-%m-%d')} au {max_date.strftime('%Y-%m-%d')}")
        
        # Afficher la période recherchée
        if time_filter == "Jour (24h)":
            search_period = f"Dernières 24h depuis {(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M')}"
        elif time_filter == "Semaine (7j)":
            search_period = f"7 derniers jours depuis {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}"
        elif time_filter == "Mois (30j)":
            search_period = f"30 derniers jours depuis {(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')}"
        elif time_filter == "Année (365j)":
            search_period = f"365 derniers jours depuis {(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')}"
        else:
            search_period = time_filter
        
        st.info(f"📅 Filtre cherche: {search_period}")

# ════════════════════════════════════════════════════════════════
# MÉTRIQUES - SELON LA PÉRIODE SÉLECTIONNÉE
# ════════════════════════════════════════════════════════════════
st.subheader(f"📊 Performance - {time_filter}")

col1, col2, col3, col4 = st.columns(4)

# ✅ Utiliser df_filtered (données selon le filtre sélectionné)
if not df_filtered.empty and 'profit' in df_filtered.columns:
    total_pnl = float(df_filtered['profit'].sum())
else:
    total_pnl = 0

total_trades = len(df_filtered) if not df_filtered.empty else 0

if not df_filtered.empty and 'result' in df_filtered.columns:
    wins = len(df_filtered[df_filtered['result'] == 'WIN'])
else:
    wins = 0

win_rate = (wins / total_trades * 100) if total_trades > 0 else 0

if not df_filtered.empty and 'profit' in df_filtered.columns and 'result' in df_filtered.columns and wins > 0:
    avg_profit = float(df_filtered[df_filtered['result'] == 'WIN']['profit'].mean())
else:
    avg_profit = 0

with col1:
    st.metric("💰 PNL Total", f"{total_pnl:.2f} €", 
             delta=f"{total_pnl:.2f} €" if total_pnl > 0 else None)

with col2:
    st.metric("📊 Total Trades", total_trades)

with col3:
    st.metric("🎯 Win Rate", f"{win_rate:.1f}%",
             delta=f"{win_rate - 50:.1f}%" if win_rate != 0 else None)

with col4:
    st.metric("📈 Profit Moyen", f"{avg_profit:.2f} €")

# Informations sur les sessions
st.markdown("---")
st.subheader("📅 Sessions Chargées")

col1, col2 = st.columns(2)
with col1:
    st.metric("🗂️ Nombre de Sessions", len(sessions_info))
with col2:
    if sessions_info:
        last_session = max(s['date'] for s in sessions_info)
        st.metric("📆 Dernière Session", last_session)

# Graphique PnL cumulatif
st.markdown("---")
st.subheader("📈 PnL Cumulatif")

if 'profit' in df_filtered.columns and 'timestamp_close' in df_filtered.columns:
    df_cumul = df_filtered.sort_values('timestamp_close').copy()
    df_cumul['pnl_cumul'] = df_cumul['profit'].cumsum()
    
    fig = px.line(df_cumul, x='timestamp_close', y='pnl_cumul',
                 labels={'timestamp_close': 'Date', 'pnl_cumul': 'PnL Cumulé (€)'},
                 title="Évolution du PnL")
    fig.update_traces(line_color='#000000', line_width=2)
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#000000')
    )
    st.plotly_chart(fig, use_container_width=True)

# Performance par session
st.markdown("---")
st.subheader("📊 Performance par Session")

if not df_sessions.empty:
    df_sessions_display = df_sessions.sort_values('date', ascending=False).copy()
    
    # Ajouter la colonne time si disponible
    if 'time' in df_sessions_display.columns:
        df_sessions_display['Date/Heure'] = df_sessions_display['date'] + ' ' + df_sessions_display['time']
    else:
        df_sessions_display['Date/Heure'] = df_sessions_display['date']
    
    # Formatter les colonnes
    df_sessions_display['PNL'] = df_sessions_display['total_pnl'].apply(lambda x: f"{x:+.2f} €")
    df_sessions_display['Win Rate'] = df_sessions_display['win_rate'].apply(lambda x: f"{x:.1f}%")
    df_sessions_display['Trades'] = df_sessions_display['total_trades'].astype(int)
    df_sessions_display['Wins'] = df_sessions_display['wins'].astype(int)
    df_sessions_display['Losses'] = df_sessions_display['losses'].astype(int)
    
    # Sélectionner les colonnes à afficher
    display_columns = ['Date/Heure', 'Trades', 'Wins', 'Losses', 'Win Rate', 'PNL']
    
    st.dataframe(
        df_sessions_display[display_columns],
        use_container_width=True,
        hide_index=True
    )

# 📅 CALENDRIER VISUEL - Jour Rouge/Vert
st.markdown("---")
st.subheader("📅 Calendrier des Performances")

if 'timestamp_close' in df_trades.columns and 'profit' in df_trades.columns:
    # Calculer PnL par jour
    df_daily = df_trades.copy()
    df_daily['date'] = df_daily['timestamp_close'].dt.date
    daily_pnl = df_daily.groupby('date')['profit'].sum().reset_index()
    daily_pnl.columns = ['date', 'pnl']
    daily_pnl['date'] = pd.to_datetime(daily_pnl['date'])
    
    # Préparer les données pour le calendrier
    daily_pnl['month'] = daily_pnl['date'].dt.strftime('%Y-%m')
    daily_pnl['day'] = daily_pnl['date'].dt.day
    daily_pnl['weekday'] = daily_pnl['date'].dt.day_name()
    daily_pnl['color'] = daily_pnl['pnl'].apply(lambda x: 'green' if x > 0 else 'red')
    
    # Créer le graphique calendrier
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📆 Jours")
        
        # Heatmap des jours
        fig_days = go.Figure(data=go.Heatmap(
            x=daily_pnl['date'],
            y=['PNL'],
            z=[daily_pnl['pnl']],
            colorscale=[
                [0, '#FF4444'],      # Rouge foncé pour pertes
                [0.5, '#FFFFFF'],    # Blanc pour 0
                [1, '#44FF44']       # Vert foncé pour gains
            ],
            text=daily_pnl['pnl'].apply(lambda x: f"{x:+.0f}€"),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='Date: %{x}<br>PNL: %{z:.2f}€<extra></extra>',
            zmid=0
        ))
        
        fig_days.update_layout(
            height=150,
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000')
        )
        
        st.plotly_chart(fig_days, use_container_width=True)
        
        # Statistiques jours
        green_days = len(daily_pnl[daily_pnl['pnl'] > 0])
        red_days = len(daily_pnl[daily_pnl['pnl'] < 0])
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("🟢 Jours Verts", green_days)
        with col_stat2:
            st.metric("🔴 Jours Rouges", red_days)
    
    with col2:
        st.markdown("### 📊 Semaines")
        
        # Calculer PnL par semaine
        df_weekly = df_trades.copy()
        df_weekly['week'] = df_weekly['timestamp_close'].dt.to_period('W').astype(str)
        weekly_pnl = df_weekly.groupby('week')['profit'].sum().reset_index()
        weekly_pnl.columns = ['week', 'pnl']
        weekly_pnl['color'] = weekly_pnl['pnl'].apply(lambda x: 'green' if x > 0 else 'red')
        
        # Heatmap des semaines
        fig_weeks = go.Figure(data=go.Heatmap(
            x=weekly_pnl['week'],
            y=['PNL'],
            z=[weekly_pnl['pnl']],
            colorscale=[
                [0, '#FF4444'],
                [0.5, '#FFFFFF'],
                [1, '#44FF44']
            ],
            text=weekly_pnl['pnl'].apply(lambda x: f"{x:+.0f}€"),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='Semaine: %{x}<br>PNL: %{z:.2f}€<extra></extra>',
            zmid=0
        ))
        
        fig_weeks.update_layout(
            height=150,
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000')
        )
        
        st.plotly_chart(fig_weeks, use_container_width=True)
        
        # Statistiques semaines
        green_weeks = len(weekly_pnl[weekly_pnl['pnl'] > 0])
        red_weeks = len(weekly_pnl[weekly_pnl['pnl'] < 0])
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("🟢 Semaines Vertes", green_weeks)
        with col_stat2:
            st.metric("🔴 Semaines Rouges", red_weeks)
    
    # ═══════════════════════════════════════════════════════════════
    # CALENDRIER MOIS ET ANNÉES
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 📅 Mois")
        
        # Calculer PnL par mois
        df_monthly = df_trades.copy()
        df_monthly['month'] = df_monthly['timestamp_close'].dt.to_period('M').astype(str)
        monthly_pnl = df_monthly.groupby('month')['profit'].sum().reset_index()
        monthly_pnl.columns = ['month', 'pnl']
        monthly_pnl['color'] = monthly_pnl['pnl'].apply(lambda x: 'green' if x > 0 else 'red')
        
        # Heatmap des mois
        fig_months = go.Figure(data=go.Heatmap(
            x=monthly_pnl['month'],
            y=['PNL'],
            z=[monthly_pnl['pnl']],
            colorscale=[
                [0, '#FF4444'],      # Rouge foncé pour pertes
                [0.5, '#FFFFFF'],    # Blanc pour 0
                [1, '#44FF44']       # Vert foncé pour gains
            ],
            text=monthly_pnl['pnl'].apply(lambda x: f"{x:+.0f}€"),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='Mois: %{x}<br>PNL: %{z:.2f}€<extra></extra>',
            zmid=0
        ))
        
        fig_months.update_layout(
            height=150,
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000')
        )
        
        st.plotly_chart(fig_months, use_container_width=True)
        
        # Statistiques mois
        green_months = len(monthly_pnl[monthly_pnl['pnl'] > 0])
        red_months = len(monthly_pnl[monthly_pnl['pnl'] < 0])
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("🟢 Mois Verts", green_months)
        with col_stat2:
            st.metric("🔴 Mois Rouges", red_months)
    
    with col4:
        st.markdown("### 📆 Années")
        
        # Calculer PnL par année
        df_yearly = df_trades.copy()
        df_yearly['year'] = df_yearly['timestamp_close'].dt.year.astype(str)
        yearly_pnl = df_yearly.groupby('year')['profit'].sum().reset_index()
        yearly_pnl.columns = ['year', 'pnl']
        yearly_pnl['color'] = yearly_pnl['pnl'].apply(lambda x: 'green' if x > 0 else 'red')
        
        # Heatmap des années
        fig_years = go.Figure(data=go.Heatmap(
            x=yearly_pnl['year'],
            y=['PNL'],
            z=[yearly_pnl['pnl']],
            colorscale=[
                [0, '#FF4444'],      # Rouge foncé pour pertes
                [0.5, '#FFFFFF'],    # Blanc pour 0
                [1, '#44FF44']       # Vert foncé pour gains
            ],
            text=yearly_pnl['pnl'].apply(lambda x: f"{x:+.0f}€"),
            texttemplate='%{text}',
            textfont={"size": 12},
            hovertemplate='Année: %{x}<br>PNL: %{z:.2f}€<extra></extra>',
            zmid=0
        ))
        
        fig_years.update_layout(
            height=150,
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000')
        )
        
        st.plotly_chart(fig_years, use_container_width=True)
        
        # Statistiques années
        green_years = len(yearly_pnl[yearly_pnl['pnl'] > 0])
        red_years = len(yearly_pnl[yearly_pnl['pnl'] < 0])
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("🟢 Années Vertes", green_years)
        with col_stat2:
            st.metric("🔴 Années Rouges", red_years)

# Tableau des derniers trades
st.markdown("---")
st.subheader("📋 Derniers Trades")

display_cols = ['timestamp_close', 'direction', 'profit', 'result', 'confidence']
if 'mt5_instance' in df_filtered.columns:
    display_cols.insert(1, 'mt5_instance')

available_cols = [col for col in display_cols if col in df_filtered.columns]

if available_cols:
    last_trades = df_filtered[available_cols].tail(20).sort_values('timestamp_close', ascending=False)
    st.dataframe(last_trades, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>ROYCE ROLLS Trading Dashboard | Mise à jour automatique via GitHub</p>
</div>
""", unsafe_allow_html=True)
