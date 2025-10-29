import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import os

# --- Configuration de la page ---
st.set_page_config(
    page_title="ROYCE ROLLS | DASHBOARD XAUUSD",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Chargement du CSS Responsive ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    body {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stApp {
        max-width: 100% !important;
        padding: 0 !important;
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
    
    .stPlotlyChart {
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px !important;
        margin: 10px 0 !important;
        padding: 10px !important;
    }
    
    .stDataFrame {
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px !important;
        margin: 10px 0 !important;
    }
    
    .stButton>button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #333333 !important;
        transform: translateY(-2px) !important;
    }
    
    .stSelectbox, .stDateInput, .stMultiselect {
        border-radius: 6px !important;
        margin: 5px 0 !important;
    }
    
    /* Responsive pour mobile */
    @media (max-width: 768px) {
        .stMetric {
            width: 100% !important;
        }
        .stPlotlyChart {
            width: 100% !important;
            height: 300px !important;
        }
        .stDataFrame {
            width: 100% !important;
            font-size: 12px !important;
        }
    }
    
    /* iPhone/iPad spécifiques */
    @media (max-width: 480px) {
        .stMetric [data-testid="stMetricValue"] {
            font-size: 20px !important;
        }
        .stPlotlyChart {
            height: 250px !important;
        }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F5F5F5 !important;
        border-right: 1px solid #E0E0E0 !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Configuration de l'Authentification ---
def load_config():
    """Charger la configuration d'authentification"""
    if not os.path.exists('config.yaml'):
        # Créer un fichier config par défaut
        default_config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'jbquesnay@gmail.com',
                        'name': 'Jean-Baptiste Quesnay',
                        'password': '$2b$12$KIXxPzQF7Jq3Z8.NZX9kzeYmVw7HQF5Kx3f9YQC.RqXm8Fz9XQW0O'  # "admin123"
                    }
                }
            },
            'cookie': {
                'name': 'royce_rolls_dashboard',
                'key': 'royce_rolls_secret_key_2024',
                'expiry_days': 30
            }
        }
        with open('config.yaml', 'w') as f:
            yaml.dump(default_config, f)
        return default_config
    
    with open('config.yaml') as file:
        return yaml.load(file, Loader=SafeLoader)

config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- Page de Login ---
name, authentication_status, username = authenticator.login(location='main')

if authentication_status == False:
    st.error('❌ Email/mot de passe incorrect')
elif authentication_status == None:
    st.warning('⚠️ Veuillez entrer votre email et mot de passe')
elif authentication_status:
    # --- Initialisation des Données Cumulatives ---
    if "cumulative_data" not in st.session_state:
        st.session_state.cumulative_data = {
            "session_summary": pd.DataFrame(),
            "daily_performance": pd.DataFrame(),
            "trades_details": pd.DataFrame(),
            "monthly_performance": pd.DataFrame()
        }

    # --- Fonction pour Charger les Données du Bot ---
    def load_bot_data():
        """Charger les données depuis trade_history.json et session_data.json"""
        data = {
            "session_summary": pd.DataFrame(),
            "daily_performance": pd.DataFrame(),
            "trades_details": pd.DataFrame(),
            "monthly_performance": pd.DataFrame()
        }
        
        # Charger trade_history.json
        if os.path.exists("trade_history.json"):
            try:
                with open("trade_history.json", "r", encoding="utf-8") as f:
                    trades = json.load(f)
                    if trades:
                        df = pd.DataFrame(trades)
                        
                        # Convertir les timestamps
                        if 'timestamp_close' in df.columns:
                            df['timestamp_close'] = pd.to_datetime(df['timestamp_close'])
                        if 'timestamp_open' in df.columns:
                            df['timestamp_open'] = pd.to_datetime(df['timestamp_open'])
                        
                        # Trades details
                        data['trades_details'] = df
                        
                        # Daily performance
                        if 'timestamp_close' in df.columns and 'profit' in df.columns:
                            daily = df.groupby(df['timestamp_close'].dt.date).agg({
                                'profit': 'sum',
                                'trade_id': 'count',
                                'result': lambda x: (x == 'WIN').sum() / len(x) * 100 if len(x) > 0 else 0
                            }).reset_index()
                            daily.columns = ['date', 'pnl', 'trades', 'win_rate']
                            data['daily_performance'] = daily
                        
                        # Monthly performance
                        if 'timestamp_close' in df.columns and 'profit' in df.columns:
                            df['month'] = df['timestamp_close'].dt.to_period('M')
                            monthly = df.groupby('month').agg({
                                'profit': 'sum',
                                'trade_id': 'count',
                                'result': lambda x: (x == 'WIN').sum() / len(x) * 100 if len(x) > 0 else 0
                            }).reset_index()
                            monthly['date'] = monthly['month'].astype(str)
                            monthly = monthly[['date', 'profit', 'trade_id', 'result']]
                            monthly.columns = ['date', 'pnl', 'trades', 'win_rate']
                            data['monthly_performance'] = monthly
            except Exception as e:
                st.error(f"Erreur lors du chargement de trade_history.json: {e}")
        
        return data

    # --- Fonction pour Charger les Données Existantes ---
    def load_existing_data():
        if os.path.exists("cumulative_data.json"):
            try:
                with open("cumulative_data.json", "r") as f:
                    data = json.load(f)
                    st.session_state.cumulative_data = {
                        "session_summary": pd.DataFrame(data.get("session_summary", [])),
                        "daily_performance": pd.DataFrame(data.get("daily_performance", [])),
                        "trades_details": pd.DataFrame(data.get("trades_details", [])),
                        "monthly_performance": pd.DataFrame(data.get("monthly_performance", []))
                    }
            except Exception as e:
                st.error(f"Erreur lors du chargement des données: {e}")

    # --- Fonction pour Sauvegarder les Données ---
    def save_cumulative_data():
        try:
            with open("cumulative_data.json", "w") as f:
                json.dump({
                    "session_summary": st.session_state.cumulative_data["session_summary"].to_dict(orient="records"),
                    "daily_performance": st.session_state.cumulative_data["daily_performance"].to_dict(orient="records"),
                    "trades_details": st.session_state.cumulative_data["trades_details"].to_dict(orient="records"),
                    "monthly_performance": st.session_state.cumulative_data["monthly_performance"].to_dict(orient="records")
                }, f, indent=4, default=str)
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde: {e}")

    # --- Fonction pour Supprimer une Session ---
    def delete_session(end_time):
        try:
            session_date = pd.to_datetime(end_time).date()
            st.session_state.cumulative_data["session_summary"] = st.session_state.cumulative_data["session_summary"][
                st.session_state.cumulative_data["session_summary"]["end_time"] != end_time
            ]
            
            if not st.session_state.cumulative_data["trades_details"].empty and 'timestamp_close' in st.session_state.cumulative_data["trades_details"].columns:
                st.session_state.cumulative_data["trades_details"]['timestamp_close'] = pd.to_datetime(st.session_state.cumulative_data["trades_details"]['timestamp_close'])
                st.session_state.cumulative_data["trades_details"] = st.session_state.cumulative_data["trades_details"][
                    ~st.session_state.cumulative_data["trades_details"]["timestamp_close"].dt.date.eq(session_date)
                ]
            
            if not st.session_state.cumulative_data["daily_performance"].empty:
                st.session_state.cumulative_data["daily_performance"] = st.session_state.cumulative_data["daily_performance"][
                    st.session_state.cumulative_data["daily_performance"]["date"] != str(session_date)
                ]
            
            save_cumulative_data()
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {e}")

    # --- Chargement Initial ---
    load_existing_data()

    # --- Barre Latérale pour Navigation ---
    st.sidebar.title(f"👤 {name}")
    authenticator.logout(location='sidebar')
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "📍 Navigation",
        ["📊 Dashboard", "📁 Charger Données", "🗑️ Supprimer Session"],
        label_visibility="collapsed"
    )

    # --- Page 1: Dashboard Principal ---
    if page == "📊 Dashboard":
        st.title("📈 ROYCE ROLLS | DASHBOARD XAUUSD")
        
        # Charger automatiquement les données du bot
        if st.sidebar.button("🔄 Actualiser depuis le Bot"):
            bot_data = load_bot_data()
            st.session_state.cumulative_data.update(bot_data)
            save_cumulative_data()
            st.sidebar.success("✅ Données actualisées!")
            st.rerun()
        
        # Vérifier si des données existent
        if st.session_state.cumulative_data["trades_details"].empty:
            st.info("ℹ️ Aucune donnée disponible. Chargez les données du bot ou importez des fichiers.")
            
            # Bouton pour charger automatiquement
            if st.button("📥 Charger les données du bot"):
                bot_data = load_bot_data()
                st.session_state.cumulative_data.update(bot_data)
                save_cumulative_data()
                st.success("✅ Données chargées!")
                st.rerun()
        else:
            # Filtres de période
            st.sidebar.markdown("---")
            st.sidebar.header("🔍 Filtres")
            time_filter = st.sidebar.radio(
                "Période",
                ["Tout", "Jour", "Semaine", "Mois", "Année", "Personnalisé"],
                horizontal=False
            )
            
            # Logique de filtre
            df_trades = st.session_state.cumulative_data["trades_details"].copy()
            
            if not df_trades.empty and 'timestamp_close' in df_trades.columns:
                df_trades['timestamp_close'] = pd.to_datetime(df_trades['timestamp_close'])
                
                if time_filter == "Jour":
                    df_trades = df_trades[df_trades['timestamp_close'].dt.date == datetime.now().date()]
                elif time_filter == "Semaine":
                    week_ago = datetime.now() - timedelta(days=7)
                    df_trades = df_trades[df_trades['timestamp_close'] >= week_ago]
                elif time_filter == "Mois":
                    month_ago = datetime.now() - timedelta(days=30)
                    df_trades = df_trades[df_trades['timestamp_close'] >= month_ago]
                elif time_filter == "Année":
                    year_ago = datetime.now() - timedelta(days=365)
                    df_trades = df_trades[df_trades['timestamp_close'] >= year_ago]
                elif time_filter == "Personnalisé":
                    col1, col2 = st.sidebar.columns(2)
                    start_date = col1.date_input("Début", datetime.now() - timedelta(days=30))
                    end_date = col2.date_input("Fin", datetime.now())
                    df_trades = df_trades[
                        (df_trades['timestamp_close'].dt.date >= start_date) &
                        (df_trades['timestamp_close'].dt.date <= end_date)
                    ]
            
            # Métriques principales
            if not df_trades.empty:
                col1, col2, col3, col4 = st.columns(4)
                
                total_pnl = df_trades['profit'].sum() if 'profit' in df_trades.columns else 0
                total_trades = len(df_trades)
                wins = len(df_trades[df_trades['result'] == 'WIN']) if 'result' in df_trades.columns else 0
                win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
                avg_profit = df_trades[df_trades['result'] == 'WIN']['profit'].mean() if wins > 0 else 0
                
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
                
                # Graphique PnL cumulatif
                st.markdown("---")
                st.subheader("📈 PnL Cumulatif")
                
                if 'profit' in df_trades.columns and 'timestamp_close' in df_trades.columns:
                    df_cumul = df_trades.sort_values('timestamp_close').copy()
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
                
                # Tableau des derniers trades
                st.markdown("---")
                st.subheader("📋 Derniers Trades")
                
                display_cols = ['timestamp_close', 'direction', 'profit', 'result', 'confidence']
                available_cols = [col for col in display_cols if col in df_trades.columns]
                
                if available_cols:
                    last_trades = df_trades[available_cols].tail(20).sort_values('timestamp_close', ascending=False)
                    st.dataframe(last_trades, use_container_width=True)

    # --- Page 2: Chargement de Données ---
    elif page == "📁 Charger Données":
        st.title("📁 Importer des Données")
        
        st.markdown("""
        ### Options de chargement :
        1. **Automatique** : Charger depuis les fichiers du bot (`trade_history.json`)
        2. **Manuel** : Importer des fichiers personnalisés
        """)
        
        tab1, tab2 = st.tabs(["🤖 Automatique", "📤 Manuel"])
        
        with tab1:
            st.subheader("Chargement Automatique")
            
            if os.path.exists("trade_history.json"):
                st.success("✅ Fichier `trade_history.json` détecté")
                
                if st.button("📥 Charger les données"):
                    bot_data = load_bot_data()
                    st.session_state.cumulative_data.update(bot_data)
                    save_cumulative_data()
                    st.success("✅ Données chargées avec succès!")
                    st.balloons()
            else:
                st.warning("⚠️ Fichier `trade_history.json` non trouvé")
        
        with tab2:
            st.subheader("Import Manuel")
            
            uploaded_file = st.file_uploader(
                "Importer trade_history.json",
                type=["json"],
                help="Sélectionnez le fichier trade_history.json"
            )
            
            if uploaded_file and st.button("📥 Charger"):
                try:
                    trades = json.load(uploaded_file)
                    df = pd.DataFrame(trades)
                    st.session_state.cumulative_data["trades_details"] = df
                    save_cumulative_data()
                    st.success("✅ Données importées avec succès!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erreur: {e}")

    # --- Page 3: Suppression des Sessions ---
    elif page == "🗑️ Supprimer Session":
        st.title("🗑️ Supprimer des Sessions")
        
        if not st.session_state.cumulative_data["trades_details"].empty:
            df = st.session_state.cumulative_data["trades_details"]
            
            if 'timestamp_close' in df.columns:
                df['date'] = pd.to_datetime(df['timestamp_close']).dt.date
                sessions = df.groupby('date').agg({
                    'profit': 'sum',
                    'trade_id': 'count'
                }).reset_index()
                sessions.columns = ['Date', 'PNL (€)', 'Trades']
                
                st.dataframe(sessions, use_container_width=True)
                
                dates_to_delete = st.multiselect(
                    "Sélectionnez les dates à supprimer",
                    options=sessions['Date'].tolist(),
                    format_func=lambda x: f"{x} (PNL: {sessions[sessions['Date'] == x]['PNL (€)'].values[0]:.2f}€)"
                )
                
                if st.button("🗑️ Supprimer", type="primary"):
                    if dates_to_delete:
                        for date in dates_to_delete:
                            delete_session(str(date))
                        st.success("✅ Sessions supprimées!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Aucune session sélectionnée")
        else:
            st.info("ℹ️ Aucune donnée disponible")

