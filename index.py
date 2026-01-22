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
        st.error(f"Erro ao conectar com Supabase: {e}")
        return None

supabase = init_connection()

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Adição da logo e data (Mantido)
logo_file = "PPM(LOGOBRANCA).png"
logo_base64 = get_base64_of_bin_file(logo_file)
data_hoje = datetime.now().strftime("%d/%m/%Y")
hora_hoje = datetime.now().strftime("%H:%M")

# --- DESIGN SYSTEM "DARK MODERN SAAS" (BASEADO NO REACT) ---
# Cores extraídas do tailwind.config.ts e index.css da referência
LOVABLE_CSS = """
    <style>
        /* Import tipografia Inter (Padrão do React) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Variáveis de Cor - STONE 950 THEME */
        :root {
            --background: #0c0a09;       /* Stone 950 - Fundo Geral */
            --card-bg: #1c1917;          /* Stone 900 - Fundo Cards */
            --border: #292524;           /* Stone 800 - Bordas */
            --text-primary: #fafaf9;     /* Stone 50 - Texto Principal */
            --text-secondary: #a8a29e;   /* Stone 400 - Texto Secundário */
            --primary-orange: #dd490e;   /* Laranja Oficial do Projeto */
            --glow-color: rgba(221, 73, 14, 0.2); /* Glow Laranja */
            --success: #22c55e;
        }

        /* Reset Global */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: var(--text-primary) !important;
            background-color: var(--background) !important;
        }

        /* Fundo da Aplicação */
        .stApp {
            background-color: var(--background) !important;
        }

        /* Ocultar elementos padrão */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
        }

        /* --- BARRA SUPERIOR (HEADER) --- */
        .lovable-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--card-bg);
            border-bottom: 1px solid var(--border);
            padding: 1rem 1.5rem;
            margin: -1rem -1.5rem 1.5rem -1.5rem;
            box-shadow: 0 4px 20px -5px rgba(0,0,0,0.5);
        }
        .header-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .header-meta {
            font-size: 0.875rem;
            color: var(--text-secondary);
            font-family: monospace;
            display: flex;
            gap: 15px;
        }

        /* --- CARDS METRICA (Estilo React) --- */
        div.metric-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        div.metric-card:hover {
            border-color: var(--primary-orange);
            box-shadow: 0 0 20px -5px var(--glow-color);
        }
        /* Efeito de brilho no canto */
        div.metric-card::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, var(--glow-color) 0%, transparent 60%);
            opacity: 0.5;
            pointer-events: none;
        }
        .metric-label {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.1;
        }
        .metric-sub {
            font-size: 0.875rem;
            color: var(--primary-orange);
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        /* --- PODIUM (RANKING) --- */
        .podium-container {
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
            height: 250px;
        }
        .podium-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            border-radius: 8px 8px 0 0;
            padding: 1rem;
            width: 100%;
            position: relative;
            transition: all 0.3s ease;
        }
        /* 1º Lugar */
        .step-1 {
            height: 100%;
            background: linear-gradient(180deg, rgba(221, 73, 14, 0.2) 0%, rgba(221, 73, 14, 0.05) 100%);
            border: 1px solid var(--primary-orange);
            border-bottom: none;
            box-shadow: 0 -10px 40px -10px var(--glow-color);
        }
        /* 2º e 3º Lugar */
        .step-secondary {
            height: 70%;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-bottom: none;
        }
        .podium-rank {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .podium-name {
            font-weight: 700;
            font-size: 1rem;
            text-align: center;
            color: var(--text-primary);
        }
        .podium-score {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: 4px;
        }

        /* --- TABELA (DATAFRAME) --- */
        [data-testid="stDataFrame"] {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        [data-testid="stDataFrame"] div {
            color: var(--text-secondary) !important;
        }
    </style>
"""
st.markdown(LOVABLE_CSS, unsafe_allow_html=True)

# --- HEADER RENDERIZADO (HTML) ---
st.markdown(f"""
    <div class="lovable-header">
        <div class="header-title">
            <span style="color: #dd490e; font-size: 24px;">🔥</span>
            Painel de Agendamento & Captação
        </div>
        <div class="header-meta">
            <div>📍 RECIFE</div>
            <div style="color: #dd490e;">● {data_hoje} {hora_hoje}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# AQUI DEVE ENTRAR A SUA LÓGICA DE DADOS (CARREGAMENTO, DATAFRAMES)
# Mantenha suas queries do Supabase, cálculos de 'top3', 'faturamento', etc.
# ---------------------------------------------------------------------

# ... (SEU CÓDIGO DE LÓGICA AQUI) ...

# ---------------------------------------------------------------------
# EXEMPLOS DE COMO USAR O NOVO VISUAL (Substitua pelos seus dados reais)
# ---------------------------------------------------------------------

# LAYOUT GRID
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    # Exemplo: Card de Última Conversão
    # Use f-strings com suas variáveis: f"{ultima_conversao_valor}"
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Última Conversão</div>
            <div class="metric-value">R$ 4.500</div>
            <div class="metric-sub">
                <span>⚡</span> Há 12 minutos
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Exemplo: Card de Top Operador (Estilo simples)
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Top Operador</div>
            <div class="metric-value">Alexandre</div>
            <div class="metric-sub" style="color: #22c55e;">
                <span>▲</span> 15 Agendamentos
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    # Exemplo: Card de Meta
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Meta Diária</div>
            <div class="metric-value">82%</div>
            <div class="metric-sub">
                <span>🎯</span> Faltam 8 leads
            </div>
        </div>
    """, unsafe_allow_html=True)

# ESPAÇAMENTO
st.markdown("<br>", unsafe_allow_html=True)

# SEÇÃO DE RANKING (PODIUM) - VISUAL ATUALIZADO
# Certifique-se de que a variável 'top3' existe na sua lógica
# Exemplo de estrutura esperada para 'top3': [{'nome': 'Alexandre', 'vendas': 10}, ...]

st.markdown("""
    <div style="background: #1c1917; border: 1px solid #292524; border-radius: 12px; padding: 20px;">
        <h3 style="color: #fafaf9; font-size: 16px; text-transform: uppercase; margin-bottom: 10px;">🏆 Ranking de Performance</h3>
        <div class="podium-container">
            <div class="podium-step step-secondary">
                <div class="podium-rank">🥈</div>
                <div class="podium-name">João</div>
                <div class="podium-score">8 Vendas</div>
            </div>
            <div class="podium-step step-1">
                <div class="podium-rank">👑</div>
                <div class="podium-name">Alexandre</div>
                <div class="podium-score" style="color: #dd490e; font-weight: bold;">15 Vendas</div>
            </div>
            <div class="podium-step step-secondary">
                <div class="podium-rank">🥉</div>
                <div class="podium-name">Pedro</div>
                <div class="podium-score">5 Vendas</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
