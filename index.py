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

# --- Design System Lovable / Modern SaaS (Tailwind-inspired) ---
# Cores: slate-50 fundo, cards brancos, rounded-2xl, shadow-sm, laranja em destaque
LOVABLE_CSS = """
    <style>
        /* Import tipografia moderna */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

        /* Reset / base */
        html, body, [class*="css"] {
            font-family: 'DM Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }

        /* Fundo slate-50 */
        .stApp {
            background-color: #f8fafc !important;
            background: #f8fafc !important;
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

        /* Barra superior - clean, sombra suave */
        .lovable-topbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 64px;
            background: #ffffff;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.5rem;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05);
            border-bottom: 1px solid #e2e8f0;
        }
        .lovable-topbar img { height: 40px; object-fit: contain; }
        .lovable-topbar-right {
            text-align: right;
            color: #1e293b;
            font-size: 0.875rem;
            font-weight: 500;
        }
        .lovable-topbar-title { font-size: 1.125rem; font-weight: 600; margin: 0; color: #0f172a; }
        .lovable-topbar-meta { font-size: 0.8rem; color: #64748b; margin-top: 2px; }
        .lovable-spacer { height: 64px; }

        /* Cards Lovable: white, rounded-2xl, shadow-sm */
        .lovable-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            border: 1px solid #f1f5f9;
            margin-bottom: 1rem;
            transition: box-shadow 0.2s ease, border-color 0.2s ease;
        }
        .lovable-card:hover {
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
            border-color: #e2e8f0;
        }

        /* Bento grid container */
        .lovable-bento {
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 1rem;
            width: 100%;
        }
        @media (max-width: 900px) {
            .lovable-bento { grid-template-columns: 1fr; }
        }

        /* Labels / títulos de seção */
        .lovable-label {
            font-size: 0.75rem;
            color: #64748b;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        .lovable-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.25;
            letter-spacing: -0.02em;
            margin: 0.25rem 0 0.75rem 0;
        }

        /* Badge - laranja com moderação */
        .lovable-badge {
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .lovable-badge-orange {
            background: #fff7ed;
            color: #c2410c;
            border: 1px solid #fed7aa;
        }
        .lovable-badge-green {
            background: #f0fdf4;
            color: #166534;
            border: 1px solid #bbf7d0;
        }
        .lovable-badge-blue {
            background: #eff6ff;
            color: #1d4ed8;
            border: 1px solid #bfdbfe;
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
            border-radius: 16px;
            background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            box-shadow: 0 1px 3px 0 rgb(249 115 22 / 0.25);
        }
        .lovable-avatar-name { font-size: 1.25rem; font-weight: 600; color: #1e293b; }

        /* Pódio - bento style */
        .lovable-podium {
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 0.75rem;
            height: 220px;
            margin-top: 1rem;
        }
        .lovable-podium-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            border-radius: 16px 16px 0 0;
            width: 32%;
            padding: 1rem 0.75rem 0.75rem;
            background: #ffffff;
            border: 1px solid #f1f5f9;
            box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        }
        .lovable-podium-step-1 {
            height: 100%;
            order: 2;
            background: #fff7ed;
            border-color: #fed7aa;
            box-shadow: 0 2px 4px -1px rgb(249 115 22 / 0.1);
        }
        .lovable-podium-step-2 { height: 70%; order: 1; }
        .lovable-podium-step-3 { height: 55%; order: 3; }
        .lovable-podium-name { font-size: 0.9rem; font-weight: 600; color: #475569; margin-bottom: 0.25rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%; text-align: center; }
        .lovable-podium-count { font-size: 1.5rem; font-weight: 800; color: #f97316; line-height: 1; }
        .lovable-podium-rank { font-size: 0.7rem; color: #94a3b8; font-weight: 500; margin-top: 0.25rem; text-transform: uppercase; letter-spacing: 0.05em; }

        /* Header da tabela - mesmo estilo dos cards, colado ao dataframe */
        .lovable-table-header {
            background: #ffffff;
            border-radius: 16px 16px 0 0;
            padding: 1rem 1.5rem;
            border: 1px solid #f1f5f9;
            border-bottom: none;
            box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            margin-bottom: 0;
        }

        /* Tabela Streamlit - override para Lovable (bento card) */
        [data-testid="stDataFrame"] {
            background: #ffffff !important;
            border-radius: 0 0 16px 16px !important;
            padding: 0 1.5rem 1.5rem !important;
            border: 1px solid #f1f5f9 !important;
            border-top: none !important;
            box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05) !important;
            margin-top: 0 !important;
        }
        [data-testid="stDataFrame"] div[data-testid="stVerticalBlock"] { background: transparent !important; }
        [data-testid="glide-cell"] {
            background: transparent !important;
            color: #475569 !important;
            border-color: #f1f5f9 !important;
            padding: 0.75rem 1rem !important;
        }
        [data-testid="glide-cell"] > div { color: #475569 !important; font-weight: 400; }
        [data-testid="glide-header-cell"] {
            background: #f8fafc !important;
            color: #1e293b !important;
            font-weight: 600 !important;
            border-bottom: 1px solid #e2e8f0 !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.8rem;
        }
        [data-testid="stDataFrame"] table { border-collapse: separate; border-spacing: 0; }
        [data-testid="glide-row"]:hover { background-color: #fff7ed !important; }

        /* Esconder blocos vazios do Streamlit entre nossos cards */
        .stColumn > div:empty { display: none !important; }
    </style>
"""

st.markdown(LOVABLE_CSS, unsafe_allow_html=True)

if logo_base64:
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo PPM">'
else:
    img_tag = '<span style="color:#64748b;font-weight:600;">PPM</span>'

st.markdown(f"""
    <div class="lovable-topbar">
        <div class="lovable-topbar-left">{img_tag}</div>
        <div class="lovable-topbar-right">
            <div class="lovable-topbar-title">Dashboard — Agendamento & Captação</div>
            <div class="lovable-topbar-meta">{hora_hoje} · {data_hoje}</div>
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
            <div class="lovable-label">Última conversão realizada</div>
            <div class="lovable-title">{latest.get('nome_cartao', '---')}</div>
            <span class="lovable-badge {badge_cls}">{texto_esteira}</span>
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
            <div class="lovable-label" style="text-align:center; border-bottom:1px solid #f1f5f9; padding-bottom:0.75rem; margin-bottom:1rem;">🏆 Ranking de conversões</div>
            <div class="lovable-podium">
                <div class="lovable-podium-step lovable-podium-step-2">
                    <div class="lovable-podium-name">{top3[1]['nome'].split()[0] if top3[1]['nome'] != '-' else '-'}</div>
                    <div class="lovable-podium-count">{top3[1]['count']}</div>
                    <div class="lovable-podium-rank">2º</div>
                </div>
                <div class="lovable-podium-step lovable-podium-step-1">
                    <div class="lovable-podium-name">{top3[0]['nome'].split()[0] if top3[0]['nome'] != '-' else '-'}</div>
                    <div class="lovable-podium-count">{top3[0]['count']}</div>
                    <div class="lovable-podium-rank">1º</div>
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

