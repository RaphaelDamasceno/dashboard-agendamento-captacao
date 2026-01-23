import streamlit as st
import pandas as pd
from supabase import create_client
import time
import base64
from datetime import datetime
import textwrap
from html import escape 
import re 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard PPM",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNÇÕES AUXILIARES ---
def clean_html(html_str):
    return textwrap.dedent(html_str).strip()

def sanitize_text(text):
    if not isinstance(text, str): return str(text)
    clean = re.sub('<[^<]+?>', '', text)
    return escape(clean)

def sanitize_df(df):
    if df.empty: return df
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: sanitize_text(x) if isinstance(x, str) else x)
    return df

# --- CONEXÃO SUPABASE ---
SUPABASE_URL = "https://ypyjwaypvhoebyralnlg.supabase.co"
SUPABASE_KEY = "sb_secret_teGZUf0kJWuSZw3J7kVtSA_2UQnHArZ"

@st.cache_resource
def init_connection():
    try: return create_client(SUPABASE_URL, SUPABASE_KEY)
    except: return None

supabase = init_connection()

# --- DESIGN SYSTEM (CSS REFORMULADO) ---
ORANGE_PPM = "#F15A24" # O laranja exato da marca

LOVABLE_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    :root {{
        --bg-app: #F4F4F4;
        --primary: {ORANGE_PPM};
        --text-main: #1A1A1A;
    }}

    .stApp {{
        background-color: var(--bg-app);
    }}

    /* Faixa Laranja de Fundo */
    .orange-header-bg {{
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 220px;
        background-color: var(--primary);
        z-index: 0;
    }}

    header, footer, #MainMenu {{ visibility: hidden; }}
    
    .block-container {{
        padding: 2rem 3rem !important;
        position: relative;
        z-index: 1;
    }}

    /* Topbar */
    .topbar {{
        display: flex; justify-content: space-between; align-items: center;
        background: white;
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}

    /* Cards Gerais */
    .card {{
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        height: 100%;
    }}

    /* Hero Card */
    .hero-title {{
        font-size: 2.8rem;
        font-weight: 800;
        color: #1A1A1A;
        line-height: 1.1;
        margin: 1rem 0;
        letter-spacing: -0.02em;
    }}
    .hero-subtitle {{
        color: #B26B4D;
        text-transform: uppercase;
        font-weight: 700;
        font-size: 0.85rem;
        display: flex; align-items: center; justify-content: center; gap: 8px;
    }}
    .hero-badge {{
        border: 1.5px solid #B26B4D;
        color: #B26B4D;
        padding: 6px 20px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1.5rem;
    }}

    /* Pódio (Igual à Imagem) */
    .podium-box {{
        display: flex; align-items: flex-end; justify-content: center;
        gap: 15px; height: 180px; margin-top: 20px;
    }}
    .podium-col {{
        flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
        border-radius: 12px; position: relative;
    }}
    .col-1 {{ 
        height: 140px; background: white; border: 2px solid var(--primary); 
        color: var(--text-main); order: 2;
    }}
    .col-2 {{ 
        height: 110px; background: var(--primary); color: white; order: 1;
    }}
    .col-3 {{ 
        height: 90px; background: var(--primary); color: white; order: 3;
    }}
    
    .podium-val {{ font-size: 1.8rem; font-weight: 800; }}
    .podium-label {{ font-size: 0.7rem; font-weight: 600; text-transform: uppercase; opacity: 0.9; }}

    /* Histórico */
    .history-item {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 12px 0; border-bottom: 1px solid #F0F0F0;
    }}
    .h-name {{ font-weight: 600; color: #333; }}
    .h-time {{ color: #999; font-size: 0.85rem; min-width: 60px; }}
    .h-tag {{
        border: 1.5px solid #B26B4D; color: #B26B4D;
        padding: 2px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 800;
    }}

    /* Animação Live */
    .live-dot {{
        height: 8px; width: 8px; background-color: #ff4b4b;
        border-radius: 50%; display: inline-block;
        margin-right: 5px; animation: blink 1.5s infinite;
    }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
</style>
<div class="orange-header-bg"></div>
"""
st.markdown(LOVABLE_CSS, unsafe_allow_html=True)

# --- DATA FETCHING ---
def get_data():
    try:
        response = supabase.table("vendas_dashboard").select("*").order("data_conclusao", desc=True).limit(50).execute()
        return sanitize_df(pd.DataFrame(response.data))
    except:
        return pd.DataFrame()

df = get_data()

if df.empty:
    st.warning("Sem dados disponíveis.")
    st.stop()

# --- TOPBAR ---
st.markdown(clean_html(f"""
    <div class="topbar">
        <div style="display:flex; align-items:center; gap:20px;">
            <span style="font-weight:800; color:{ORANGE_PPM}; font-size:1.2rem;">PRONTO <br><small style="font-weight:400; font-size:0.6rem; letter-spacing:2px; color:#333;">PRA MORAR</small></span>
            <div style="width:1px; height:30px; background:#EEE;"></div>
            <span style="font-weight:600; font-size:1rem; color:#444;">Monitoramento de Agendamentos</span>
        </div>
        <div style="background:#FFF; padding:6px 15px; border-radius:30px; border:1px solid #EEE; font-size:0.75rem; font-weight:700; color:#444; display:flex; align-items:center;">
            <span class="live-dot"></span> AO VIVO
        </div>
    </div>
"""), unsafe_allow_html=True)

# --- LAYOUT ---
col_left, col_right = st.columns([1.6, 1], gap="large")

with col_left:
    latest = df.iloc[0]
    nome_resp = latest.get('responsavel', 'Responsável')
    iniciais = "".join([n[0] for n in nome_resp.split()[:2]]).upper()
    
    st.markdown(clean_html(f"""
        <div class="card" style="text-align:center;">
            <div class="hero-subtitle">🔥 ÚLTIMA CONVERSÃO</div>
            <div class="hero-title">{latest.get('nome_cartao', 'Indefinido')}</div>
            <div class="hero-badge">AGENDAMENTO REALIZADO</div>
            <hr style="border:0; border-top:1px solid #F0F0F0; width:60%; margin: 2rem auto;">
            <div style="display:flex; flex-direction:column; align-items:center;">
                <div style="width:100px; height:100px; background:{ORANGE_PPM}; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:2.2rem; font-weight:700; margin-bottom:1rem; box-shadow: 0 8px 20px rgba(241, 90, 36, 0.3);">
                    {iniciais}
                </div>
                <div style="font-size:1.5rem; font-weight:700;">{nome_resp}</div>
                <div style="color:#999; font-size:0.9rem; margin-top:5px;">🕒 Hoje às {pd.to_datetime(latest['data_conclusao']).strftime("%H:%M")}</div>
            </div>
        </div>
    """), unsafe_allow_html=True)

with col_right:
    # Ranking para o pódio
    ranking = df['responsavel'].value_counts().reset_index().head(3).to_dict('records')
    while len(ranking) < 3: ranking.append({'responsavel': '-', 'count': 0})

    st.markdown(clean_html(f"""
        <div class="card" style="padding: 1.5rem;">
            <div style="text-align:center; color:#999; font-size:0.75rem; font-weight:800; text-transform:uppercase; letter-spacing:1px;">🏆 Top Performers</div>
            <div class="podium-box">
                <div class="podium-col col-2">
                    <div style="font-size:0.8rem; font-weight:600;">{ranking[1]['responsavel'].split()[0]}</div>
                    <div class="podium-val">{ranking[1]['count']}</div>
                    <div class="podium-label">2º</div>
                </div>
                <div class="podium-col col-1">
                    <div style="color:{ORANGE_PPM}; position:absolute; top:10px;">👑</div>
                    <div style="font-size:0.9rem; font-weight:700;">{ranking[0]['responsavel'].split()[0]}</div>
                    <div class="podium-val" style="color:{ORANGE_PPM}; font-size:2.2rem;">{ranking[0]['count']}</div>
                    <div class="podium-label" style="color:{ORANGE_PPM}">1º</div>
                </div>
                <div class="podium-col col-3">
                    <div style="font-size:0.8rem; font-weight:600;">{ranking[2]['responsavel'].split()[0]}</div>
                    <div class="podium-val">{ranking[2]['count']}</div>
                    <div class="podium-label">3º</div>
                </div>
            </div>
        </div>
        <div style="margin: 1.5rem 0 0.5rem 0; color:#999; font-size:0.75rem; font-weight:800; text-transform:uppercase; display:flex; align-items:center; gap:8px;">
            📈 Histórico Recente
        </div>
    """), unsafe_allow_html=True)

    # Lista de histórico
    history_html_content = '<div class="card" style="padding: 1rem 1.5rem;">'
    for _, row in df.head(7).iterrows():
        tipo = "CAPTAÇÃO" if str(row.get('id_esteira')) == '10' else "AGEND."
        try:
            hora = pd.to_datetime(row['data_conclusao']).strftime("%H:%M")
        except:
            hora = "-"
        nome = str(row['responsavel']).split()[0] if row.get('responsavel') else '-'
        history_html_content += f'<div class="history-item"><div style="display:flex; align-items:center; gap:15px;"><span class="h-time">{hora}</span><span class="h-name">{nome}</span></div><span class="h-tag">{tipo}</span></div>'
    history_html_content += '</div>'
    
    # Renderizar HTML diretamente
    st.markdown(history_html_content, unsafe_allow_html=True)

# Auto-refresh (usando placeholder para não bloquear)
auto_refresh_placeholder = st.empty()
with auto_refresh_placeholder.container():
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    
    if st.session_state.auto_refresh:
        time.sleep(10)
        st.rerun()
