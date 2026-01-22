import streamlit as st
import pandas as pd
from supabase import create_client
import time
import base64
from datetime import datetime
import textwrap
from html import escape 
import re 

# --- FUNÇÕES DE LIMPEZA E BLINDAGEM ---
def clean_html(html_str):
    return textwrap.dedent(html_str).strip()

def sanitize_text(text):
    if not isinstance(text, str):
        return str(text)
    clean = re.sub('<[^<]+?>', '', text)
    return escape(clean)

def sanitize_df(df):
    if df.empty:
        return df
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: sanitize_text(x) if isinstance(x, str) else x)
    return df

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="PPM - Live Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONEXÃO SUPABASE ---
SUPABASE_URL = "https://ypyjwaypvhoebyralnlg.supabase.co"
SUPABASE_KEY = "sb_secret_teGZUf0kJWuSZw3J7kVtSA_2UQnHArZ"

@st.cache_resource
def init_connection():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

supabase = init_connection()

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# --- ASSETS ---
logo_file = "PPM(LOGOBRANCA).png"
logo_base64 = get_base64_of_bin_file(logo_file)

# --- CSS: IDENTIDADE VISUAL DARK/ORANGE ---
DARK_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600;800&display=swap');

    :root {
        --bg-deep: #000000;
        --bg-card: #0f0f0f;
        --border: #1a1a1a;
        --primary: #ff4d00;
        --primary-glow: rgba(255, 77, 0, 0.4);
        --text-main: #ffffff;
        --text-muted: #888888;
        --accent-green: #00ff88;
        --accent-blue: #00d9ff;
    }

    /* Reset Geral */
    .stApp { background-color: var(--bg-deep) !important; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* Topbar */
    .ppm-topbar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 1.5rem 3rem; background: rgba(0,0,0,0.8);
        border-bottom: 1px solid var(--border); margin-bottom: 2rem;
    }
    .logo-img { height: 40px; }
    .live-status {
        display: flex; align-items: center; gap: 8px;
        color: var(--accent-green); font-weight: 800; font-size: 0.8rem;
        background: rgba(0, 255, 136, 0.1); padding: 6px 14px; border-radius: 50px;
    }

    /* Cards e Layout */
    .main-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 2rem; padding: 0 3rem; }
    
    .hero-container {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: 24px; padding: 3rem; position: relative;
        overflow: hidden; min-height: 500px; display: flex; flex-direction: column; justify-content: center;
    }
    .hero-container::before {
        content: ""; position: absolute; top: -100px; left: -100px;
        width: 300px; height: 300px; background: var(--primary-glow);
        filter: blur(100px); border-radius: 50%; pointer-events: none;
    }

    .label-mini {
        color: var(--primary); font-weight: 800; font-size: 0.9rem;
        text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;
    }

    .hero-title {
        font-family: 'Archivo Black', sans-serif;
        font-size: 5rem; line-height: 0.95; color: var(--primary);
        margin-bottom: 4rem; text-transform: uppercase;
    }

    /* Métricas Inferiores */
    .metrics-row { display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 2rem; border-top: 1px solid var(--border); padding-top: 2rem; }
    .metric-box { display: flex; align-items: center; gap: 15px; }
    .metric-icon { 
        width: 48px; height: 48px; background: #1a1a1a; 
        border-radius: 12px; display: flex; align-items: center; justify-content: center;
        color: var(--primary); border: 1px solid #222;
    }
    .metric-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 2px; }
    .metric-value { font-size: 1.4rem; font-weight: 800; color: var(--text-main); }

    /* Ranking & Histórico */
    .side-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 24px; padding: 2rem; margin-bottom: 2rem; }
    .side-title { 
        font-size: 1.2rem; font-weight: 800; color: var(--text-main); margin-bottom: 1.5rem;
        display: flex; align-items: center; gap: 10px;
    }

    .ranking-row {
        display: flex; align-items: center; justify-content: space-between;
        padding: 12px 15px; background: #151515; border-radius: 12px; margin-bottom: 8px;
        border: 1px solid transparent; transition: 0.3s;
    }
    .ranking-row:hover { border-color: var(--primary); background: #1a1a1a; }
    .rank-number { font-weight: 900; color: var(--primary); width: 25px; }
    .rank-name { font-weight: 600; color: var(--text-main); flex: 1; margin-left: 10px; }
    .rank-count { font-weight: 800; color: var(--primary); background: rgba(255,77,0,0.1); padding: 4px 10px; border-radius: 6px; }

    .history-row {
        display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid #1a1a1a;
    }
    .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--primary); }
    .hist-time { color: var(--text-muted); font-family: monospace; font-size: 0.85rem; }
    .hist-name { color: var(--text-main); font-weight: 500; flex: 1; }
    .badge {
        font-size: 0.65rem; font-weight: 900; padding: 4px 10px; border-radius: 4px; text-transform: uppercase;
    }
    .badge-agend { color: var(--accent-blue); background: rgba(0, 217, 255, 0.1); }
    .badge-capt { color: var(--accent-green); background: rgba(0, 255, 136, 0.1); }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .dot-live { animation: pulse 1.5s infinite; }
</style>
"""

# --- RENDERIZAÇÃO ---
st.markdown(clean_html(DARK_THEME_CSS), unsafe_allow_html=True)

# TOPBAR
if logo_base64:
    img_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img">'
else:
    img_html = '<h1 style="color:white; margin:0;">PPM</h1>'

st.markdown(clean_html(f"""
    <div class="ppm-topbar">
        {img_html}
        <div class="live-status">
            <span class="dot-live">●</span> AO VIVO
        </div>
    </div>
"""), unsafe_allow_html=True)

# DATA FETCH
def get_data():
    try:
        response = supabase.table("vendas_dashboard").select("*").order("data_conclusao", desc=True).limit(50).execute()
        return sanitize_df(pd.DataFrame(response.data))
    except Exception:
        return pd.DataFrame()

df = get_data()

if df.empty:
    st.markdown("<h2 style='color:white; text-align:center;'>Aguardando novos agendamentos...</h2>", unsafe_allow_html=True)
else:
    latest = df.iloc[0]
    
    # Grid Principal
    st.markdown('<div class="main-grid">', unsafe_allow_html=True)
    
    # COLUNA ESQUERDA (HERO)
    with st.container():
        nome_cartao = latest.get('nome_cartao', '---').upper()
        nome_resp = latest.get('responsavel', 'Indefinido')
        id_esteira = str(latest.get('id_esteira', '0'))
        is_captacao = id_esteira == '10'
        tipo_lead = "CAPTAÇÃO" if is_captacao else "AGENDAMENTO"
        hora = pd.to_datetime(latest['data_conclusao']).strftime("%H:%M")

        st.markdown(clean_html(f"""
            <div class="hero-container">
                <div class="label-mini">🔥 ÚLTIMA CONVERSÃO</div>
                <div class="hero-title">{nome_cartao}</div>
                
                <div class="metrics-row">
                    <div class="metric-box">
                        <div class="metric-icon">👤</div>
                        <div>
                            <div class="metric-label">Responsável</div>
                            <div class="metric-value">{nome_resp}</div>
                        </div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-icon">🚀</div>
                        <div>
                            <div class="metric-label">Esteira</div>
                            <div class="metric-value">{tipo_lead} PREMIUM</div>
                        </div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-icon">🕒</div>
                        <div>
                            <div class="metric-label">Horário</div>
                            <div class="metric-value">{hora}</div>
                        </div>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

    # COLUNA DIREITA (SIDE)
    with st.container():
        # Ranking
        ranking_df = df['responsavel'].value_counts().reset_index()
        ranking_df.columns = ['nome', 'count']
        
        rank_html = '<div class="side-card"><div class="side-title">🏆 RANKING DO DIA</div>'
        for i, row in ranking_df.head(5).iterrows():
            rank_html += f"""
            <div class="ranking-row">
                <span class="rank-number">{i+1}º</span>
                <span class="rank-name">{row['nome']}</span>
                <span class="rank-count">{row['count']}</span>
            </div>
            """
        rank_html += '</div>'
        st.markdown(rank_html, unsafe_allow_html=True)

        # Histórico
        hist_html = '<div class="side-card"><div class="side-title">🕒 HISTÓRICO</div>'
        for _, row in df.head(8).iterrows():
            badge_class = "badge-capt" if str(row.get('id_esteira')) == '10' else "badge-agend"
            label = "CAPTAÇÃO" if str(row.get('id_esteira')) == '10' else "AGENDAMENTO"
            hist_html += f"""
            <div class="history-row">
                <div class="dot"></div>
                <div class="hist-time">{pd.to_datetime(row['data_conclusao']).strftime("%H:%M")}</div>
                <div class="hist-name">{row['responsavel'].split()[0]}</div>
                <div class="badge {badge_class}">{label}</div>
            </div>
            """
        hist_html += '</div>'
        st.markdown(hist_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh
time.sleep(5)
st.rerun()
