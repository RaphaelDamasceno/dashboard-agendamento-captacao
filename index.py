# Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
from supabase import create_client
import time
import base64
from datetime import datetime

# Configuração da página (título e visualização). Usarei wide pois é um projeto voltado para TVs
st.set_page_config(
    page_title="Dashboard PPM",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Conexão com a Base de Dados do Supabase, utilizando o URL do projeto e a secret key
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

# Adição da logo na barra superior
logo_file = "PPM(LOGOBRANCA).png"
logo_base64 = get_base64_of_bin_file(logo_file)

# Adição de data e hora
data_hoje = datetime.now().strftime("%d/%m/%Y")
hora_hoje = datetime.now().strftime("%H:%M")

# --- Design System Lovable / Modern SaaS (Dark Stone & Orange Theme) ---
# Cores: Stone 950 fundo, Cards Stone 900, Orange (#dd490e) destaques
LOVABLE_CSS = """
    <style>
        /* Import tipografia moderna Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Variáveis de Tema (Baseado no Tailwind Config do React) */
        :root {
            --background: #0c0a09;       /* Stone 950 */
            --card-bg: #1c1917;          /* Stone 900 */
            --border: #292524;           /* Stone 800 */
            --text-primary: #fafaf9;     /* Stone 50 */
            --text-secondary: #a8a29e;   /* Stone 400 */
            --primary-orange: #dd490e;   /* Laranja Principal */
            --glow: rgba(221, 73, 14, 0.15);
        }

        /* Reset / base */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: var(--text-primary) !important;
            background-color: var(--background) !important;
        }

        /* Fundo da Aplicação */
        .stApp {
            background-color: var(--background) !important;
        }

        /* Remover padding excessivo - layout clean */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 100% !important;
        }

        header { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }

        /* Barra superior - Dark, sem borda branca */
        .lovable-topbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 64px;
            background: rgba(28, 25, 23, 0.8); /* Stone 900 com transparência */
            backdrop-filter: blur(10px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.5rem;
            border-bottom: 1px solid var(--border);
            box-shadow: 0 4px 20px -5px rgba(0,0,0,0.5);
        }
        .lovable-topbar img { height: 35px; object-fit: contain; opacity: 0.9; }
        .lovable-topbar-right {
            text-align: right;
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
            font-family: monospace;
        }
        .lovable-topbar-title { 
            font-size: 1.125rem; 
            font-weight: 600; 
            margin: 0; 
            color: var(--text-primary);
            display: flex; 
            align-items: center; 
            gap: 8px;
        }
        .lovable-spacer { height: 80px; }

        /* Cards Lovable: Dark Stone, Borda Sutil, Glow no Hover */
        .lovable-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid var(--border);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        
        .lovable-card:hover {
            border-color: var(--primary-orange);
            box-shadow: 0 0 30px -5px var(--glow);
        }

        /* Labels / títulos de seção dentro dos cards */
        .lovable-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.1em;
            margin-bottom: 0.75rem;
        }
        .lovable-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.2;
            letter-spacing: -0.02em;
            margin: 0.25rem 0 1rem 0;
        }

        /* Badges - Cores ajustadas para Dark Mode */
        .lovable-badge {
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        /* Captação: Verde neon escuro */
        .lovable-badge-green {
            background: rgba(34, 197, 94, 0.1);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.2);
        }
        /* Agendamento: Azul neon escuro */
        .lovable-badge-blue {
            background: rgba(59, 130, 246, 0.1);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        /* Avatar responsável */
        .lovable-avatar-wrap {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 1rem 0;
        }
        .lovable-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #dd490e 0%, #9a3412 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
            box-shadow: 0 0 20px rgba(221, 73, 14, 0.4);
            border: 2px solid rgba(255,255,255,0.1);
        }
        .lovable-avatar-name { 
            font-size: 1.25rem; 
            font-weight: 600; 
            color: var(--text-primary); 
        }

        /* Pódio - Estilo Dark */
        .lovable-podium {
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 1rem;
            height: 220px;
            margin-top: 1rem;
        }
        .lovable-podium-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            border-radius: 8px 8px 0 0;
            width: 32%;
            padding: 1rem 0.5rem 0.5rem;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-bottom: none;
            transition: all 0.3s;
        }
        /* 1º Lugar - Destaque Laranja */
        .lovable-podium-step-1 {
            height: 100%;
            order: 2;
            background: linear-gradient(180deg, rgba(221, 73, 14, 0.15) 0%, rgba(28, 25, 23, 0) 100%);
            border-color: var(--primary-orange);
            box-shadow: 0 -10px 30px -10px rgba(221, 73, 14, 0.3);
            z-index: 2;
        }
        .lovable-podium-step-2 { height: 70%; order: 1; }
        .lovable-podium-step-3 { height: 55%; order: 3; }
        
        .lovable-podium-name { 
            font-size: 0.9rem; 
            font-weight: 600; 
            color: var(--text-primary); 
            margin-bottom: 0.25rem; 
            text-align: center;
            white-space: nowrap; 
            overflow: hidden; 
            text-overflow: ellipsis; 
            width: 100%; 
        }
        .lovable-podium-count { 
            font-size: 1.5rem; 
            font-weight: 800; 
            color: var(--text-primary); 
            line-height: 1; 
        }
        /* Cor do número do ranking no pódio */
        .lovable-podium-step-1 .lovable-podium-count { color: var(--primary-orange); }

        .lovable-podium-rank { 
            font-size: 0.7rem; 
            color: var(--text-secondary); 
            font-weight: 500; 
            margin-top: 0.5rem; 
        }

        /* Header da Tabela */
        .lovable-table-header {
            background: var(--card-bg);
            border-radius: 12px 12px 0 0;
            padding: 1rem 1.5rem;
            border: 1px solid var(--border);
            border-bottom: none;
            margin-bottom: 0;
        }

        /* Tabela Streamlit - Adaptação Dark Mode */
        [data-testid="stDataFrame"] {
            background: var(--card-bg) !important;
            border-radius: 0 0 12px 12px !important;
            padding: 0 1rem 1rem !important;
            border: 1px solid var(--border) !important;
            border-top: none !important;
        }
        /* Corrigindo cores da tabela interna */
        [data-testid="stDataFrame"] div[data-testid="stVerticalBlock"] { background: transparent !important; }
        [data-testid="glide-cell"] {
            background: transparent !important;
            color: var(--text-secondary) !important;
            border-color: var(--border) !important;
        }
        [data-testid="glide-header-cell"] {
            background: #292524 !important; /* Stone 800 header */
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            border-bottom: 1px solid var(--border) !important;
            text-transform: uppercase;
            font-size: 0.75rem;
        }
        [data-testid="glide-row"]:hover { background-color: rgba(255,255,255,0.05) !important; }
        
        /* Ajuste fino para colunas vazias */
        .stColumn > div:empty { display: none !important; }
    </style>
"""

st.markdown(LOVABLE_CSS, unsafe_allow_html=True)

if logo_base64:
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo PPM">'
else:
    img_tag = '<span style="color:#dd490e;font-weight:700;font-size:20px;">PPM</span>'

st.markdown(f"""
    <div class="lovable-topbar">
        <div class="lovable-topbar-left">
            <div class="lovable-topbar-title">
                {img_tag}
                <span style="margin-left:10px; opacity:0.2;">|</span>
                <span style="margin-left:10px;">Dashboard</span>
            </div>
        </div>
        <div class="lovable-topbar-right">
            <div style="color: #dd490e;">● AO VIVO</div>
            <div class="lovable-topbar-meta">{data_hoje} — {hora_hoje}</div>
        </div>
    </div>
    <div class="lovable-spacer"></div>
""", unsafe_allow_html=True)


def get_data():
    try:
        response = supabase.table("vendas_dashboard").select("*").order("data_conclusao", desc=True).limit(100).execute()
        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        return pd.DataFrame()


df = get_data()

if df.empty:
    st.info("Aguardando dados...")
else:
    col_left, col_right = st.columns([1, 1.2], gap="medium")

    with col_left:
        latest = df.iloc[0]
        id_esteira = str(latest.get('id_esteira', '0'))
        is_captacao = id_esteira == '10'
        texto_esteira = "Captação" if is_captacao else "Agendamento"
        badge_cls = "lovable-badge-green" if is_captacao else "lovable-badge-blue"

        nome_resp = latest.get('responsavel', 'Indefinido')
        iniciais = "".join([n[0] for n in nome_resp.split()[:2]]).upper()

        st.markdown(f"""
        <div class="lovable-card">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div>
                    <div class="lovable-label">Última conversão realizada</div>
                    <div class="lovable-title">{latest.get('nome_cartao', '---')}</div>
                    <span class="lovable-badge {badge_cls}">{texto_esteira}</span>
                </div>
                <div style="font-size:24px;">💰</div>
            </div>
        </div>

        <div class="lovable-card">
            <div class="lovable-label" style="text-align:center;">Responsável pela conversão</div>
            <div class="lovable-avatar-wrap">
                <div class="lovable-avatar">{iniciais}</div>
                <div class="lovable-avatar-name">{nome_resp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        ranking_df = df['responsavel'].value_counts().reset_index()
        ranking_df.columns = ['nome', 'count']
        top3 = ranking_df.head(3).to_dict('records')
        while len(top3) < 3:
            top3.append({'nome': '-', 'count': 0})

        st.markdown(f"""
        <div class="lovable-card">
            <div class="lovable-label" style="text-align:center; border-bottom:1px solid #292524; padding-bottom:0.75rem; margin-bottom:1rem;">
                🏆 Ranking de Performance
            </div>
            <div class="lovable-podium">
                <div class="lovable-podium-step lovable-podium-step-2">
                    <div class="lovable-podium-name">{top3[1]['nome'].split()[0] if top3[1]['nome'] != '-' else '-'}</div>
                    <div class="lovable-podium-count">{top3[1]['count']}</div>
                    <div class="lovable-podium-rank">2º</div>
                </div>
                <div class="lovable-podium-step lovable-podium-step-1">
                    <div class="lovable-podium-name">{top3[0]['nome'].split()[0] if top3[0]['nome'] != '-' else '-'}</div>
                    <div class="lovable-podium-count">{top3[0]['count']}</div>
                    <div class="lovable-podium-rank" style="color:#dd490e;">👑 1º</div>
                </div>
                <div class="lovable-podium-step lovable-podium-step-3">
                    <div class="lovable-podium-name">{top3[2]['nome'].split()[0] if top3[2]['nome'] != '-' else '-'}</div>
                    <div class="lovable-podium-count">{top3[2]['count']}</div>
                    <div class="lovable-podium-rank">3º</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="lovable-table-header">
                <div class="lovable-label" style="margin-bottom:0;">📋 Lista detalhada (histórico)</div>
            </div>
        """, unsafe_allow_html=True)

        view_df = df[['responsavel', 'nome_cartao', 'id_esteira', 'data_conclusao']].copy()
        view_df['Esteira'] = view_df['id_esteira'].apply(lambda x: "Captação" if str(x) == '10' else "Agendamento")
        view_df['Data/Hora'] = pd.to_datetime(view_df['data_conclusao']).dt.strftime('%d/%m %H:%M')

        st.dataframe(
            view_df[['responsavel', 'nome_cartao', 'Esteira', 'Data/Hora']],
            column_config={
                "responsavel": "Responsável",
                "nome_cartao": "Nome do Cartão",
                "Esteira": st.column_config.TextColumn("Esteira"),
                "Data/Hora": "Conclusão"
            },
            hide_index=True,
            use_container_width=True,
            height=300
        )

# Auto-refresh
time.sleep(5)
st.rerun()
