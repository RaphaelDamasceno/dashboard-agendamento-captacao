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

# --- CONEXÃO SUPABASE (INTOCADA) ---
SUPABASE_URL = "https://ypyjwaypvhoebyralnlg.supabase.co"
SUPABASE_KEY = "sb_secret_teGZUf0kJWuSZw3J7kVtSA_2UQnHArZ"

@st.cache_resource
def init_connection():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        # st.error(f"Erro conexão: {e}") # Silenciado para produção
        return None

supabase = init_connection()

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# --- ASSETS & ÍCONES (SVG LUCIDE REAIS) ---
# Extraídos diretamente da biblioteca Lucide usada no React para máxima fidelidade
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

# --- DESIGN SYSTEM "DARK MODERN SAAS" (CSS AVANÇADO) ---
LOVABLE_CSS = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        :root {
            /* Cores HSL exatas do seu index.css */
            --bg-app: #0c0a09;       /* Stone 950 */
            --bg-card: #181514;      /* Stone 925 (Ajustado para contraste) */
            --border: #292524;       /* Stone 800 */
            --text-main: #fafaf9;    /* Stone 50 */
            --text-muted: #a8a29e;   /* Stone 400 */
            --primary: #dd490e;      /* Laranja Principal */
            --primary-glow: rgba(221, 73, 14, 0.3);
            --glass: rgba(255, 255, 255, 0.03);
        }

        /* Reset Global */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: var(--text-main) !important;
            background-color: var(--bg-app) !important;
        }
        
        /* Layout Fixes */
        .stApp { background-color: var(--bg-app) !important; }
        header, footer, #MainMenu { visibility: hidden; }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
        }

        /* --- TOPBAR (Glass Effect) --- */
        .lovable-topbar {
            display: flex; justify-content: space-between; align-items: center;
            padding: 0.75rem 1.5rem;
            background: rgba(12, 10, 9, 0.7);
            border-bottom: 1px solid var(--border);
            margin-bottom: 2rem;
            border-radius: 12px;
            backdrop-filter: blur(12px); /* Desfoque estilo Apple/Modern SaaS */
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }

        /* --- CARDS AVANÇADOS --- */
        .lovable-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 20px -5px rgba(0,0,0,0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Efeito de brilho laranja suave no topo (como na imagem de referência) */
        .lovable-card::after {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, var(--border), transparent);
        }

        /* --- HERO CARD (ESQUERDA) --- */
        .hero-card {
            height: 100%;
            display: flex; flex-direction: column; justify-content: center;
            /* Gradiente radial sutil no fundo para dar profundidade */
            background: radial-gradient(circle at 100% 0%, rgba(221, 73, 14, 0.08) 0%, transparent 50%), var(--bg-card);
            border: 1px solid rgba(221, 73, 14, 0.2);
        }
        .hero-card:hover {
            box-shadow: 0 0 40px -10px rgba(221, 73, 14, 0.15);
            border-color: rgba(221, 73, 14, 0.4);
        }

        /* Tipografia Hero */
        .label {
            font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; 
            letter-spacing: 0.1em; font-weight: 600; margin-bottom: 0.5rem;
            display: flex; align-items: center; gap: 6px;
        }
        .value-huge {
            font-size: 3rem; font-weight: 800; color: var(--text-main); line-height: 1.1;
            letter-spacing: -0.03em;
        }
        
        /* Avatar Animado */
        .avatar-glow {
            width: 80px; height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #dd490e, #c2410c);
            color: white;
            font-size: 2rem; font-weight: 700;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 25px var(--primary-glow);
            border: 2px solid rgba(255,255,255,0.1);
            position: relative;
        }
        /* Icone de status flutuante no avatar */
        .avatar-status {
            position: absolute; bottom: 0; right: 0;
            background: #0c0a09; border-radius: 50%; padding: 4px;
            color: #22c55e;
        }

        /* --- RANKING (PODIUM) --- */
        .podium-container {
            display: flex; align-items: flex-end; justify-content: center; gap: 12px;
            height: 200px; margin-top: 1rem;
        }
        .podium-bar {
            width: 32%; border-radius: 8px 8px 0 0;
            display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
            padding-bottom: 1rem;
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border); border-bottom: none;
            position: relative;
        }
        
        /* 1º Lugar - Estilo Gold/Orange Premium */
        .podium-1 {
            height: 100%; 
            background: linear-gradient(180deg, rgba(221, 73, 14, 0.15) 0%, rgba(221, 73, 14, 0.02) 100%);
            border-color: var(--primary);
            box-shadow: 0 -10px 40px -20px var(--primary-glow);
            z-index: 2;
        }
        .podium-2 { height: 75%; }
        .podium-3 { height: 60%; }

        .rank-badge {
            margin-bottom: 8px; color: var(--primary);
        }

        /* --- TABELA CLEAN --- */
        [data-testid="stDataFrame"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }
        [data-testid="glide-header-cell"] {
            background-color: #292524 !important;
            color: var(--text-muted) !important;
            font-size: 0.75rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }
        [data-testid="glide-cell"] {
            color: var(--text-main) !important;
            border-color: #292524 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Badges de Status (Pílulas) */
        .badge {
            display: inline-flex; align-items: center; gap: 6px;
            padding: 4px 10px; border-radius: 20px;
            font-size: 0.75rem; font-weight: 600; letter-spacing: 0.02em;
        }
        .badge-green { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.2); }
        .badge-blue { background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }
        
        /* SVG Icons Helpers */
        .icon-sm svg { width: 16px; height: 16px; }
        .icon-md svg { width: 20px; height: 20px; }
        .icon-lg svg { width: 24px; height: 24px; }
    </style>
"""
st.markdown(LOVABLE_CSS, unsafe_allow_html=True)

# --- HEADER/TOPBAR ---
if logo_base64:
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" style="height:32px;">'
else:
    img_tag = f'<span style="color:#dd490e; font-weight:800; font-size:20px; display:flex; align-items:center; gap:8px;">{ICONS["flame"]} PPM</span>'

st.markdown(f"""
    <div class="lovable-topbar">
        <div style="display:flex; align-items:center; gap:16px;">
            {img_tag}
            <div style="width:1px; height:24px; background:var(--border);"></div>
            <span style="font-weight:600; font-size:15px; letter-spacing:-0.01em;">Monitoramento de Vendas</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; font-family:monospace; color:var(--primary); font-size:13px; background:rgba(221,73,14,0.1); padding:4px 10px; border-radius:6px;">
            <span style="animation: pulse 2s infinite;">●</span> AO VIVO
        </div>
    </div>
""", unsafe_allow_html=True)

# --- DADOS & LÓGICA ---
def get_data():
    try:
        response = supabase.table("vendas_dashboard").select("*").order("data_conclusao", desc=True).limit(100).execute()
        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        return pd.DataFrame()

df = get_data()

# --- LAYOUT 60/40 (AGORA COM VISUAL FIEL) ---
if df.empty:
    st.info("Aguardando dados...")
else:
    col_left, col_right = st.columns([3, 2], gap="large")

    # --- ESQUERDA: HERO CARD (Última Conversão) ---
    with col_left:
        latest = df.iloc[0]
        id_esteira = str(latest.get('id_esteira', '0'))
        is_captacao = id_esteira == '10'
        
        # Configuração Dinâmica do Badge
        badge_class = "badge-green" if is_captacao else "badge-blue"
        badge_text = "CAPTAÇÃO" if is_captacao else "AGENDAMENTO"
        badge_icon = ICONS['activity'] if is_captacao else ICONS['clock']
        
        nome_resp = latest.get('responsavel', 'Indefinido')
        iniciais = "".join([n[0] for n in nome_resp.split()[:2]]).upper()
        nome_cartao = latest.get('nome_cartao', '---')
        tempo = pd.to_datetime(latest['data_conclusao']).strftime("%H:%M")

        st.markdown(f"""
            <div class="lovable-card hero-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:2rem;">
                    <div>
                        <div class="label"><span class="icon-sm">{ICONS['trending']}</span> ÚLTIMA CONVERSÃO</div>
                        <div style="font-size:3rem; font-weight:700; margin-top:0.5rem; letter-spacing:-0.02em; line-height:1.2;">
                            {nome_cartao}
                        </div>
                    </div>
                    <div class="badge {badge_class}">
                        <span class="icon-sm">{badge_icon}</span> {badge_text}
                    </div>
                </div>
                
                <div style="display:flex; align-items:center; gap:1.5rem; padding-top:2rem; border-top:1px solid var(--border);">
                    <div class="avatar-glow">
                        {iniciais}
                        <div class="avatar-status">{ICONS['flame']}</div>
                    </div>
                    <div>
                        <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:4px;">Fechado por</div>
                        <div style="font-size:1.5rem; font-weight:600; color:var(--text-main);">{nome_resp}</div>
                        <div style="font-size:0.85rem; color:var(--primary); margin-top:2px; display:flex; align-items:center; gap:4px;">
                            {ICONS['clock']} Hoje às {tempo}
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- DIREITA: RANKING + HISTÓRICO ---
    with col_right:
        # Lógica Ranking
        ranking_df = df['responsavel'].value_counts().reset_index()
        ranking_df.columns = ['nome', 'count']
        top3 = ranking_df.head(3).to_dict('records')
        while len(top3) < 3: top3.append({'nome': '-', 'count': 0})

        # Card Ranking
        st.markdown(f"""
            <div class="lovable-card" style="margin-bottom: 1.5rem; padding-bottom: 0;">
                <div class="label" style="display:flex; justify-content:space-between;">
                    <span>TOP PERFORMERS</span>
                    <span>{data_hoje}</span>
                </div>
                <div class="podium-container">
                    <div class="podium-bar podium-2">
                        <div style="font-weight:600; font-size:0.9rem; margin-bottom:4px;">{top3[1]['nome'].split()[0]}</div>
                        <div style="color:var(--text-muted); font-size:0.85rem; margin-bottom:8px;">{top3[1]['count']} vendas</div>
                        <div style="font-size:0.75rem; opacity:0.5;">2º</div>
                    </div>
                    <div class="podium-bar podium-1">
                        <div class="rank-badge">{ICONS['crown']}</div>
                        <div style="font-weight:700; color:var(--text-main); font-size:1.1rem; margin-bottom:4px;">{top3[0]['nome'].split()[0]}</div>
                        <div style="color:var(--primary); font-weight:800; font-size:1.2rem; margin-bottom:8px;">{top3[0]['count']}</div>
                    </div>
                    <div class="podium-bar podium-3">
                        <div style="font-weight:600; font-size:0.9rem; margin-bottom:4px;">{top3[2]['nome'].split()[0]}</div>
                        <div style="color:var(--text-muted); font-size:0.85rem; margin-bottom:8px;">{top3[2]['count']} vendas</div>
                        <div style="font-size:0.75rem; opacity:0.5;">3º</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Histórico (Lista Clean)
        st.markdown(f"""
            <div style="margin-bottom:10px; display:flex; align-items:center; gap:8px; color:var(--text-muted); font-size:0.85rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">
                <span class="icon-sm">{ICONS['activity']}</span> Histórico Recente
            </div>
        """, unsafe_allow_html=True)
        
        view_df = df[['responsavel', 'nome_cartao', 'id_esteira', 'data_conclusao']].copy()
        view_df['Esteira'] = view_df['id_esteira'].apply(lambda x: "Captação" if str(x) == '10' else "Agendamento")
        view_df['Hora'] = pd.to_datetime(view_df['data_conclusao']).dt.strftime('%H:%M')

        st.dataframe(
            view_df[['Hora', 'responsavel', 'Esteira']],
            column_config={
                "Hora": st.column_config.TextColumn("Horário"),
                "responsavel": st.column_config.TextColumn("Responsável"),
                "Esteira": st.column_config.TextColumn("Tipo")
            },
            hide_index=True,
            use_container_width=True,
            height=250
        )

# Auto-refresh
time.sleep(5)
st.rerun()
