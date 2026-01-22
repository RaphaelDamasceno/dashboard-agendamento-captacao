# Importação das bibliotecas necessárias (foco no streamlit)
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

# Estilização da página utilizando CSS. Apto a melhorias futuras
st.markdown(f"""
    <style>
        /* Fundo Laranja Vivo */
        .stApp {{
            background-color: #FF5722;
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        
        header {{ visibility: hidden; }}

        /* Barra superior */
        .top-bar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100px;
            background-color: #000000;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}
        
        .top-bar-left img {{
            height: 80px;
            object-fit: contain;
        }}
        
        .top-bar-right {{
            text-align: right;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }}
        
        .project-title {{ font-size: 1.8rem; font-weight: 600; margin: 0; line-height: 1.2; }}
        .project-date {{ font-size: 1.1rem; opacity: 0.8; margin: 0; }}
        .spacer {{ height: 100px; }}

        /* Componentes em branco da tela */
        .css-card {{
            background-color: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            margin-bottom: 20px;
            color: #333;
        }}

        /* Textos */
        h1, h2, h3, p, div {{ font-family: 'Segoe UI', sans-serif; }}
        .highlight-title {{ font-size: 1.1rem; color: #666; text-transform: uppercase; font-weight: bold; margin-bottom: 10px; }}
        .highlight-card-name {{ font-size: 2.2rem; font-weight: 800; color: #FF5722; line-height: 1.2; }}
        .highlight-tag {{ display: inline-block; padding: 5px 15px; border-radius: 20px; color: white; font-weight: bold; margin-top: 10px; font-size: 1rem; }}
        
        /* Avatar (sem fotos no momento) */
        .avatar-box {{ display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 20px; }}
        .avatar-circle-big {{ width: 100px; height: 100px; border-radius: 50%; background-color: #333; color: white; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 15px; }}

        /* Podium */
        .podium-container {{ display: flex; align-items: flex-end; justify-content: center; height: 220px; gap: 15px; }}
        .podium-step {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-end; border-radius: 8px 8px 0 0; color: white; font-weight: bold; text-align: center; width: 30%; padding-bottom: 10px; }}
        .step-1 {{ height: 90%; background: #fbbf24; order: 2; font-size: 2rem; box-shadow: 0 0 10px rgba(0,0,0,0.2); position: relative; z-index: 2; }}
        .step-2 {{ height: 65%; background: #9ca3af; order: 1; font-size: 1.5rem; opacity: 0.9; }}
        .step-3 {{ height: 45%; background: #b45309; order: 3; font-size: 1.2rem; opacity: 0.9; }}

        /*  */
        
        /* 1. Header do Cartão da Tabela */
        .table-header-card {{
            background-color: white;
            border-radius: 15px 15px 0 0;
            padding: 20px 25px 10px 25px;
            margin-bottom: -15px; /* Cola na tabela abaixo */
            position: relative;
            z-index: 1;
        }}

        /* 2. Container da Tabela */
        [data-testid="stDataFrame"] {{
            width: 100% !important;
            background-color: white !important;
            border-radius: 0 0 15px 15px !important;
            padding: 0 25px 25px 25px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }}

        /* 3. Forçar Cores Claras na Tabela (Fundo Branco, Texto Cinza) */
        [data-testid="stDataFrame"] div[data-testid="stVerticalBlock"] {{
            background-color: white !important;
        }}
        
        [data-testid="glide-cell"] {{
            background-color: white !important;
            color: #8F8F8F !important;
            border-color: #eee !important;
        }}
        
        /* Texto dentro das células */
        [data-testid="glide-cell"] > div {{
            color: #8F8F8F !important;
        }}

        /* Cabeçalho das Colunas */
        [data-testid="glide-header-cell"] {{
            background-color: #f9f9f9 !important;
            color: #333 !important;
            font-weight: bold !important;
            border-bottom: 1px solid #ddd !important;
        }}

    </style>
""", unsafe_allow_html=True)

if logo_base64:
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo PPM">'
else:
    img_tag = '<span style="color:white;">LOGO NÃO ENCONTRADA</span>'

st.markdown(f"""
    <div class="top-bar">
        <div class="top-bar-left">{img_tag}</div>
        <div class="top-bar-right">
            <div class="project-title">Dashboard - Agendamento & Captação</div>
            <div class="project-date">{hora_hoje} | {data_hoje}</div>
        </div>
    </div>
    <div class="spacer"></div>
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
        texto_esteira = "CAPTAÇÃO" if is_captacao else "AGENDAMENTO"
        cor_esteira = "#4ade80" if is_captacao else "#60a5fa"
        
        nome_resp = latest.get('responsavel', 'Indefinido')
        iniciais = "".join([n[0] for n in nome_resp.split()[:2]]).upper()

        st.markdown(f"""
        <div class="css-card">
            <div class="highlight-title">Última Conversão Realizada</div>
            <div class="highlight-card-name">{latest.get('nome_cartao', '---')}</div>
            <div class="highlight-tag" style="background-color: {cor_esteira};">{texto_esteira}</div>
        </div>
        
        <div class="css-card" style="min-height: 250px; display: flex; flex-direction: column; justify-content: center;">
            <div class="highlight-title" style="text-align:center;">RESPONSÁVEL PELA CONVERSÃO</div>
            <div class="avatar-box">
                <div class="avatar-circle-big">{iniciais}</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #333;">{nome_resp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        # Ranking
        ranking_df = df['responsavel'].value_counts().reset_index()
        ranking_df.columns = ['nome', 'count']
        top3 = ranking_df.head(3).to_dict('records')
        while len(top3) < 3: top3.append({'nome': '-', 'count': 0})

        st.markdown(f"""
        <div class="css-card">
            <div class="highlight-title" style="text-align: center; border-bottom: 1px solid #eee; padding-bottom: 10px;">🏆 Ranking de Conversões</div>
            <div class="podium-container">
                <div class="podium-step step-2">
                    <div style="margin-bottom:5px; font-size: 0.9rem; color: #333;">{top3[1]['nome'].split()[0]}</div>
                    <div>{top3[1]['count']}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8">2º</div>
                </div>
                <div class="podium-step step-1">
                    <div style="margin-bottom:5px; font-size: 1rem; color: #333; font-weight:bold;">{top3[0]['nome'].split()[0]}</div>
                    <div>{top3[0]['count']}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8">1º</div>
                </div>
                <div class="podium-step step-3">
                    <div style="margin-bottom:5px; font-size: 0.9rem; color: #333;">{top3[2]['nome'].split()[0]}</div>
                    <div>{top3[2]['count']}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8">3º</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Lista detalhada de dados
        st.markdown("""
            <div class="table-header-card">
                <div class="highlight-title" style="margin-bottom:0;">📋 Lista Detalhada (Histórico)</div>
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