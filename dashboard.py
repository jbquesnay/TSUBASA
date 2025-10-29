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
                
                # Ajouter les trades
                trades = session_data.get('trades', [])
                all_trades.extend(trades)
                
                # Ajouter les infos de session
                sessions_info.append({
                    'date': session_data.get('date'),
                    'timestamp': session_data.get('timestamp'),
                    'total_pnl': session_data.get('total_pnl', 0),
                    'total_trades': session_data.get('total_trades', 0),
                    'win_rate': session_data.get('win_rate', 0),
                    'wins': session_data.get('wins', 0),
                    'losses': session_data.get('losses', 0)
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

# Convertir les timestamps
if 'timestamp_close' in df_trades.columns:
    df_trades['timestamp_close'] = pd.to_datetime(df_trades['timestamp_close'])
if 'timestamp_open' in df_trades.columns:
    df_trades['timestamp_open'] = pd.to_datetime(df_trades['timestamp_open'])

# --- Filtres ---
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtres")

time_filter = st.sidebar.radio(
    "Période",
    ["Tout", "Jour", "Semaine", "Mois", "Année", "Personnalisé"],
    horizontal=False
)

# Appliquer les filtres
df_filtered = df_trades.copy()

if 'timestamp_close' in df_filtered.columns:
    if time_filter == "Jour":
        df_filtered = df_filtered[df_filtered['timestamp_close'].dt.date == datetime.now().date()]
    elif time_filter == "Semaine":
        week_ago = datetime.now() - timedelta(days=7)
        df_filtered = df_filtered[df_filtered['timestamp_close'] >= week_ago]
    elif time_filter == "Mois":
        month_ago = datetime.now() - timedelta(days=30)
        df_filtered = df_filtered[df_filtered['timestamp_close'] >= month_ago]
    elif time_filter == "Année":
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

# --- Dashboard Principal ---
st.title("📈 ROYCE ROLLS | DASHBOARD XAUUSD")

# Métriques globales
col1, col2, col3, col4 = st.columns(4)

total_pnl = df_filtered['profit'].sum() if 'profit' in df_filtered.columns else 0
total_trades = len(df_filtered)
wins = len(df_filtered[df_filtered['result'] == 'WIN']) if 'result' in df_filtered.columns else 0
win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
avg_profit = df_filtered[df_filtered['result'] == 'WIN']['profit'].mean() if wins > 0 else 0

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
    df_sessions_display['PNL'] = df_sessions_display['total_pnl'].apply(lambda x: f"{x:+.2f} €")
    df_sessions_display['Win Rate'] = df_sessions_display['win_rate'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(
        df_sessions_display[['date', 'total_trades', 'wins', 'losses', 'Win Rate', 'PNL']],
        use_container_width=True,
        hide_index=True
    )

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
