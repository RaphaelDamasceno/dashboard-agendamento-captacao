# Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
from supabase import create_client
import time
import base64
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard PPM",
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
    except Exception as e:
        return None

supabase = init_connection()

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# --- ASSETS & ÍCONES ---
ICONS = {
    "crown": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m2 4 3 12h14l3-12-6 7-4-3-4 3-6-7z"/><circle cx="12" cy="19" r="2"/></svg>""",
    "user": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>""",
    "clock": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>""",
    "activity": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>""",
    "trending": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>""",
    "flame": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.1.2-2.2.6-3a7 7 0 0 1 2.9 3.5z"/></svg>"""
}

logo_file = "PPM(LOGOBRANCA).png"
logo_base64 = get_base64_of_bin_file(logo_file)
data_hoje = datetime.now().strftime("%d/%m/%Y")
hora_hoje = datetime.now().strftime("%H:%M")

# --- DESIGN SYSTEM PPM ---
LOVABLE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-app: #0c0a09;       /* Stone 950 */
        --bg-card: #181514;      /* Stone 925 */
        --border: #292524;       /* Stone 800 */
        --text-main: #fafaf9;    /* Stone 50 */
        --text-muted: #a8a29e;   /* Stone 400 */
        --primary: #dd490e;      /* Laranja PPM Brilhante */
        --primary-glow: rgba(221, 73, 14, 0.4);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-main) !important;
        background-color: var(--bg-app) !important;
    }
    .stApp { background-color: var(--bg-app) !important; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container {
        padding: 1rem 1.5rem !important;
        max-width: 100% !important;
    }

    /* Topbar */
    .lovable-topbar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.75rem 1.5rem;
        background: rgba(12, 10, 9, 0.8);
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
        border-radius: 12px;
        backdrop-filter: blur(12px);
    }

    /* Card Base */
    .lovable-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px -5px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    .lovable-card:hover {
        border-color: var(--primary);
        box-shadow: 0 0 30px -10px var(--primary-glow);
    }

    /* Hero Card */
    .hero-card {
        height: 100%;
        display: flex; flex-direction: column; 
        align-items: center; justify-content: center;
        text-align: center;
        background: radial-gradient(circle at center, rgba(221, 73, 14, 0.05) 0%, var(--bg-card) 70%);
    }
    .hero-label {
        font-size: 0.9rem; 
        color: var(--primary);
        text-transform: uppercase; 
        letter-spacing: 0.15em; 
        font-weight: 700; 
        margin-bottom: 1rem;
        display: flex; align-items: center; gap: 8px; justify-content: center;
    }
    .hero-value {
        font-size: 3.5rem; 
        font-weight: 800; 
        color: var(--text-main); 
        line-height: 1.1;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    .hero-avatar {
        width: 90px; height: 90px;
        border-radius: 50%;
        background: linear-gradient(135deg, #dd490e, #9a3412);
        color: white;
        font-size: 2.5rem; font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 30px var(--primary-glow);
        border: 4px solid rgba(28, 25, 23, 0.8);
        margin-bottom: 1rem;
    }

    /* Ranking */
    .podium-container {
        display: flex; align-items: flex-end; justify-content: center; gap: 8px;
        height: 160px; margin-top: 1rem;
    }
    .podium-bar {
        flex: 1;
        border-radius: 8px 8px 0 0;
        display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
        padding-bottom: 0.5rem;
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border); border-bottom: none;
        position: relative;
    }
    .podium-1 {
        height: 100%; 
        background: linear-gradient(180deg, rgba(221, 73, 14, 0.2) 0%, transparent 100%);
        border-color: var(--primary);
        box-shadow: 0 -10px 30px -15px var(--primary-glow);
    }
    .podium-2 { height: 70%; }
    .podium-3 { height: 50%; }

    /* Histórico Customizado */
    .history-container {
        display: flex; flex-direction: column; gap: 8px;
        margin-top: 10px;
        max-height: 300px;
        overflow-y: auto;
        padding-right: 5px;
    }
    .history-container::-webkit-scrollbar { width: 4px; }
    .history-container::-webkit-scrollbar-track { background: transparent; }
    .history-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

    .history-row {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 10px 14px;
        transition: all 0.2s;
    }
    .history-row:hover {
        background: rgba(255,255,255,0.05);
        border-color: var(--primary);
        transform: translateX(2px);
    }
    .h-time { font-family: monospace; color: var(--text-muted); font-size: 0.8rem; }
    .h-name { font-weight: 600; color: var(--text-main); font-size: 0.9rem; margin-left: 10px; flex-grow: 1; }
    .h-badge { 
        font-size: 0.7rem; padding: 2px 8px; border-radius: 4px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;
    }
    .h-badge-green { color: #4ade80; background: rgba(74, 222, 128, 0.1); border: 1px solid rgba(74, 222, 128, 0.2); }
    .h-badge-blue { color: #60a5fa; background: rgba(96, 165, 250, 0.1); border: 1px solid rgba(96, 165, 250, 0.2); }
    
    .icon-sm svg { width: 16px; height: 16px; }
    .badge-pill {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 14px; border-radius: 20px;
        font-size: 0.8rem; font-weight: 600;
        background: rgba(12, 10, 9, 0.6);
        border: 1px solid var(--border);
    }
</style>
"""
# Removida indentação do CSS também por segurança
st.markdown(LOVABLE_CSS, unsafe_allow_html=True)

# --- HEADER ---
if logo_base64:
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" style="height:32px;">'
else:
    img_tag = f'<span style="color:#dd490e; font-weight:800; font-size:20px;">PPM</span>'

st.markdown(f"""
<div class="lovable-topbar">
    <div style="display:flex; align-items:center; gap:16px;">
        {img_tag}
        <div style="width:1px; height:24px; background:var(--border);"></div>
        <span style="font-weight:600; font-size:15px; letter-spacing:-0.01em;">Monitoramento de Agendamentos</span>
    </div>
    <div style="display:flex; align-items:center; gap:8px; font-family:monospace; color:var(--primary); font-size:13px; background:rgba(221,73,14,0.1); padding:4px 10px; border-radius:6px;">
        <span style="animation: pulse 2s infinite;">●</span> AO VIVO
    </div>
</div>
""", unsafe_allow_html=True)

# --- DADOS ---
def get_data():
    try:
        response = supabase.table("vendas_dashboard").select("*").order("data_conclusao", desc=True).limit(50).execute()
        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        return pd.DataFrame()

df = get_data()

# --- LAYOUT 60/40 ---
if df.empty:
    st.info("Aguardando dados...")
else:
    col_left, col_right = st.columns([3, 2], gap="large")

    # --- ESQUERDA: HERO CARD (CORRIGIDO: SEM INDENTAÇÃO) ---
    with col_left:
        latest = df.iloc[0]
        id_esteira = str(latest.get('id_esteira', '0'))
        is_captacao = id_esteira == '10'
        
        badge_text = "CAPTAÇÃO" if is_captacao else "AGENDAMENTO"
        badge_color = "#4ade80" if is_captacao else "#60a5fa"
        badge_style = f"color:{badge_color}; border-color:{badge_color};"
        
        nome_resp = latest.get('responsavel', 'Indefinido')
        iniciais = "".join([n[0] for n in nome_resp.split()[:2]]).upper()
        nome_cartao = latest.get('nome_cartao', '---')
        tempo = pd.to_datetime(latest['data_conclusao']).strftime("%H:%M")

        # HTML ALINHADO À ESQUERDA (COLUNA 0)
        st.markdown(f"""
<div class="lovable-card hero-card">
    <div class="hero-label">
        <span class="icon-sm">{ICONS['flame']}</span> ÚLTIMA CONVERSÃO
    </div>

    <div class="hero-value">
        {nome_cartao}
    </div>

    <div class="badge-pill" style="{badge_style} margin-bottom: 2rem;">
        {badge_text} REALIZADO
    </div>

    <div style="width: 50%; height: 1px; background: var(--border); margin-bottom: 2rem;"></div>

    <div style="display:flex; flex-direction:column; align-items:center;">
        <div class="hero-avatar">
            {iniciais}
        </div>
        <div style="font-size:1.2rem; font-weight:700; color:var(--text-main); margin-bottom:4px;">
            {nome_resp}
        </div>
        <div style="font-size:0.9rem; color:var(--text-muted); display:flex; align-items:center; gap:6px;">
            {ICONS['clock']} Hoje às {tempo}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # --- DIREITA: RANKING + HISTÓRICO ---
    with col_right:
        ranking_df = df['responsavel'].value_counts().reset_index()
        ranking_df.columns = ['nome', 'count']
        top3 = ranking_df.head(3).to_dict('records')
        while len(top3) < 3: top3.append({'nome': '-', 'count': 0})

        # RANKING (CORRIGIDO: SEM INDENTAÇÃO)
        st.markdown(f"""
<div class="lovable-card" style="margin-bottom: 1.5rem; padding-bottom: 0;">
    <div style="text-align:center; font-size:0.8rem; color:var(--text-muted); font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:10px;">
        🏆 Top Performers
    </div>
    <div class="podium-container">
        <div class="podium-bar podium-2">
            <div style="font-weight:600; font-size:0.85rem;">{top3[1]['nome'].split()[0]}</div>
            <div style="color:var(--text-muted); font-size:0.8rem;">{top3[1]['count']} Conv.</div>
            <div style="font-size:0.7rem; opacity:0.5; margin-top:2px;">2º</div>
        </div>
        <div class="podium-bar podium-1">
            <div style="color:var(--primary); margin-bottom:4px;">{ICONS['crown']}</div>
            <div style="font-weight:700; color:var(--text-main); font-size:1rem;">{top3[0]['nome'].split()[0]}</div>
            <div style="color:var(--primary); font-weight:800; font-size:1.2rem;">{top3[0]['count']}</div>
            <div style="font-size:0.7rem; color:var(--primary); margin-top:2px;">1º</div>
        </div>
        <div class="podium-bar podium-3">
            <div style="font-weight:600; font-size:0.85rem;">{top3[2]['nome'].split()[0]}</div>
            <div style="color:var(--text-muted); font-size:0.8rem;">{top3[2]['count']} Conv.</div>
            <div style="font-size:0.7rem; opacity:0.5; margin-top:2px;">3º</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

        # HISTÓRICO HEADER (CORRIGIDO: SEM INDENTAÇÃO)
        st.markdown(f"""
<div style="margin-bottom:10px; display:flex; align-items:center; gap:8px; color:var(--text-muted); font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">
    <span class="icon-sm">{ICONS['activity']}</span> Histórico Recente
</div>
""", unsafe_allow_html=True)
        
        # Gerar Lista HTML (Montagem dinâmica já estava correta, mas a div wrapper precisa ser limpa)
        html_history = '<div class="history-container">'
        
        last_records = df.head(6).to_dict('records')
        
        for record in last_records:
            r_nome = record.get('responsavel', '').split()[0]
            r_hora = pd.to_datetime(record['data_conclusao']).strftime("%H:%M")
            r_esteira = str(record.get('id_esteira', '0'))
            
            if r_esteira == '10':
                badge_html = '<span class="h-badge h-badge-green">CAPTAÇÃO</span>'
            else:
                badge_html = '<span class="h-badge h-badge-blue">AGEND.</span>'
            
            # Note que aqui dentro do loop python a indentação não afeta o output da string
            # desde que a string final seja passada limpa pro markdown, mas por garantia:
            html_history += f"""
<div class="history-row">
    <div class="h-time">{r_hora}</div>
    <div class="h-name">{r_nome}</div>
    {badge_html}
</div>"""
        
        html_history += '</div>'
        st.markdown(html_history, unsafe_allow_html=True)

# Auto-refresh
time.sleep(5)
st.rerun()
