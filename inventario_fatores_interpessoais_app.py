# app_fatores_interpessoais_final.py
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
# import matplotlib.pyplot as plt # Removido

# --- PALETA DE CORES E CONFIGURAÇÃO DA PÁGINA ---
COLOR_PRIMARY = "#70D1C6"
COLOR_TEXT_DARK = "#333333"
COLOR_BACKGROUND = "#FFFFFF"

st.set_page_config(
    page_title="Inventário — Fatores Interpessoais",
    layout="wide"
)

# --- CSS CUSTOMIZADO ---
st.markdown(f"""
    <style>
        /* Remoção de elementos do Streamlit Cloud */
        div[data-testid="stHeader"], div[data-testid="stDecoration"] {{
            visibility: hidden; height: 0%; position: fixed;
        }}
        
        /* Código que esconde o botão ping */
        #autoclick-div {{
            display: none !important; 
        }}
        
        footer {{ visibility: hidden; height: 0%; }}
        /* Estilos gerais */
        .stApp {{ background-color: {COLOR_BACKGROUND}; color: {COLOR_TEXT_DARK}; }}
        h1, h2, h3 {{ color: {COLOR_TEXT_DARK}; }}
        /* Cabeçalho customizado */
        .stApp > header {{
            background-color: {COLOR_PRIMARY}; padding: 1rem;
            border-bottom: 5px solid {COLOR_TEXT_DARK};
        }}
        /* Card de container */
        div.st-emotion-cache-1r4qj8v {{
             background-color: #f0f2f6; border-left: 5px solid {COLOR_PRIMARY};
             border-radius: 5px; padding: 1.5rem; margin-top: 1rem;
             margin-bottom: 1.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        /* Inputs e Labels */
        div[data-testid="textInputRootElement"] > label,
        div[data-testid="stTextArea"] > label,
        div[data-testid="stRadioGroup"] > label {{
            color: {COLOR_TEXT_DARK}; font-weight: 600;
        }}
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] > div,
        div[data-testid="stTextArea"] textarea {{
            border: 1px solid #cccccc;
            border-radius: 5px;
            background-color: #FFFFFF;
        }}
        /* Expanders */
        .streamlit-expanderHeader {{
            background-color: {COLOR_PRIMARY}; color: white; font-size: 1.2rem;
            font-weight: bold; border-radius: 8px; margin-top: 1rem;
            padding: 0.75rem 1rem; border: none; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .streamlit-expanderHeader:hover {{ background-color: {COLOR_TEXT_DARK}; }}
        .streamlit-expanderContent {{
            background-color: #f9f9f9; border-left: 3px solid {COLOR_PRIMARY}; padding: 1rem;
            border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; margin-bottom: 1rem;
        }}
        /* Botões de rádio (Likert) responsivos */
        div[data-testid="stRadio"] > div {{
            display: flex; flex-wrap: wrap; justify-content: flex-start;
        }}
        div[data-testid="stRadio"] label {{
            margin-right: 1.2rem; margin-bottom: 0.5rem; color: {COLOR_TEXT_DARK};
        }}
        /* Botão de Finalizar */
        .stButton button {{
            background-color: {COLOR_PRIMARY}; color: white; font-weight: bold;
            padding: 0.75rem 1.5rem; border-radius: 8px; border: none;
        }}
        .stButton button:hover {{
            background-color: {COLOR_TEXT_DARK}; color: white;
        }}
    </style>
""", unsafe_allow_html=True)
# --- CONEXÃO COM GOOGLE SHEETS (COM CACHE) ---
@st.cache_resource
def connect_to_gsheet():
    """Conecta ao Google Sheets e retorna os objetos das abas."""
    try:
        creds_dict = dict(st.secrets["google_credentials"])
        creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
        
        gc = gspread.service_account_from_dict(creds_dict)
        spreadsheet = gc.open("Respostas Formularios")
        
        # Retorna apenas a aba de respostas
        return spreadsheet.worksheet("Fatores_Interpessoais")
    except Exception as e:
        st.error(f"Erro ao conectar com o Google Sheets: {e}")
        return None

ws_respostas = connect_to_gsheet()

if ws_respostas is None:
    st.error("Não foi possível conectar à aba 'Fatores_Interpessoais' da planilha.")
    st.stop()


# --- CABEÇALHO DA APLICAÇÃO ---
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo_wedja.jpg", width=120)
    except FileNotFoundError:
        st.warning("Logo 'logo_wedja.jpg' não encontrada.")
with col2:
    st.markdown(f"""
    <div style="display: flex; align-items: center; height: 100%;">
        <h1 style='color: {COLOR_TEXT_DARK}; margin: 0; padding: 0;'>INVENTÁRIO — FATORES INTERPESSOAIS</h1>
    </div>
    """, unsafe_allow_html=True)


# --- SEÇÃO DE IDENTIFICAÇÃO ---
with st.container(border=True):
    st.markdown("<h3 style='text-align: center;'>Identificação</h3>", unsafe_allow_html=True)
    
    col1_form, col2_form = st.columns(2)
    with col1_form:
        respondente = st.text_input("Respondente:", key="input_respondente")
        data = st.text_input("Data:", datetime.now().strftime('%d/%m/%Y'))
    with col2_form:
        organizacao_coletora = st.text_input("Organização Coletora:", "Instituto Wedja de Socionomia", disabled=True)


# --- INSTRUÇÕES ---
with st.expander("Ver Orientações aos Respondentes", expanded=True):
    st.info(
        """
        - **Escala Likert 1–5:** 1=Discordo totalmente • 2=Discordo • 3=Nem discordo nem concordo • 4=Concordo • 5=Concordo totalmente.
        - Itens marcados como **(R)** são inversos para análise (a pontuação será 6 − resposta).
        """
    )


# --- LÓGICA DO QUESTIONÁRIO (BACK-END) ---
@st.cache_data
def carregar_itens():
    data = [
        ('Comunicação', 'COM01', 'As mensagens são claras e compreensíveis para todos.', 'NÃO'),
        ('Comunicação', 'COM02', 'A equipe pratica escuta ativa nas interações.', 'NÃO'),
        ('Comunicação', 'COM03', 'O feedback é frequente, respeitoso e construtivo.', 'NÃO'),
        ('Comunicação', 'COM04', 'Informações relevantes são compartilhadas com transparência.', 'NÃO'),
        ('Comunicação', 'COM05', 'Os canais de comunicação são acessíveis e bem utilizados.', 'NÃO'),
        ('Comunicação', 'COM06', 'A comunicação entre áreas é fluida e colaborativa.', 'NÃO'),
        ('Comunicação', 'COM07', 'As reuniões são objetivas, com pautas e registros.', 'NÃO'),
        ('Comunicação', 'COM08', 'Ruídos, boatos e mal-entendidos atrapalham o trabalho.', 'SIM'),
        ('Gestão de Conflitos', 'GC01', 'Conflitos são identificados e tratados logo no início.', 'NÃO'),
        ('Gestão de Conflitos', 'GC02', 'Existem critérios/processos claros para mediar conflitos.', 'NÃO'),
        ('Gestão de Conflitos', 'GC03', 'As partes são ouvidas de forma imparcial e respeitosa.', 'NÃO'),
        ('Gestão de Conflitos', 'GC04', 'Busca-se soluções que considerem os interesses de todos.', 'NÃO'),
        ('Gestão de Conflitos', 'GC05', 'É seguro discordar e expor pontos de vista diferentes.', 'NÃO'),
        ('Gestão de Conflitos', 'GC06', 'A liderança intervém quando necessário, de modo justo.', 'NÃO'),
        ('Gestão de Conflitos', 'GC07', 'Conflitos se arrastam por muito tempo sem solução.', 'SIM'),
        ('Gestão de Conflitos', 'GC08', 'Discussões descambam para ataques pessoais.', 'SIM'),
        ('Trabalho em Equipe', 'TE01', 'Há objetivos compartilhados e entendimento de prioridades.', 'NÃO'),
        ('Trabalho em Equipe', 'TE02', 'Os membros cooperam e se apoiam nas entregas.', 'NÃO'),
        ('Trabalho em Equipe', 'TE03', 'Há troca de conhecimentos e boas práticas.', 'NÃO'),
        ('Trabalho em Equipe', 'TE04', 'Papéis e responsabilidades são claros para todos.', 'NÃO'),
        ('Trabalho em Equipe', 'TE05', 'A equipe se organiza para ajudar nos picos de demanda.', 'NÃO'),
        ('Trabalho em Equipe', 'TE06', 'Existe confiança mútua entre os membros.', 'NÃO'),
        ('Trabalho em Equipe', 'TE07', 'Existem silos entre áreas ou equipes que dificultam o trabalho.', 'SIM'),
        ('Trabalho em Equipe', 'TE08', 'Há competição desleal ou sabotagem entre colegas.', 'SIM'),
        ('Respeito', 'RES01', 'As interações são cordiais e educadas.', 'NÃO'),
        ('Respeito', 'RES02', 'Horários e compromissos são respeitados.', 'NÃO'),
        ('Respeito', 'RES03', 'Contribuições são reconhecidas de forma justa.', 'NÃO'),
        ('Respeito', 'RES04', 'Interrupções desrespeitosas acontecem com frequência.', 'SIM'),
        ('Respeito', 'RES05', 'Há respeito pela diversidade de opiniões.', 'NÃO'),
        ('Respeito', 'RES06', 'A privacidade e os limites pessoais são respeitados.', 'NÃO'),
        ('Respeito', 'RES07', 'A comunicação não-violenta é incentivada e praticada.', 'NÃO'),
        ('Respeito', 'RES08', 'Piadas ofensivas ou tom agressivo são tolerados.', 'SIM'),
        ('Inclusão', 'INC01', 'Existem oportunidades iguais de participação e desenvolvimento.', 'NÃO'),
        ('Inclusão', 'INC02', 'Há representatividade de pessoas diversas em decisões.', 'NÃO'),
        ('Inclusão', 'INC03', 'Acessibilidade (linguagem, recursos) é considerada nas interações.', 'NÃO'),
        ('Inclusão', 'INC04', 'Fazem-se adaptações razoáveis quando necessário.', 'NÃO'),
        ('Inclusão', 'INC05', 'Políticas antidiscriminação são conhecidas e aplicadas.', 'NÃO'),
        ('Inclusão', 'INC06', 'As pessoas sentem que pertencem ao grupo/equipe.', 'NÃO'),
        ('Inclusão', 'INC07', 'Microagressões são toleradas ou minimizadas.', 'SIM'),
        ('Inclusão', 'INC08', 'Vozes minoritárias são ignoradas em discussões/decisões.', 'SIM'),
        ('Convicções e Valores', 'CONV01', 'Os valores organizacionais são claros e conhecidos.', 'NÃO'),
        ('Convicções e Valores', 'CONV02', 'Há coerência entre discurso e prática no dia a dia.', 'NÃO'),
        ('Convicções e Valores', 'CONV03', 'As decisões são tomadas com base em princípios éticos.', 'NÃO'),
        ('Convicções e Valores', 'CONV04', 'Há segurança para manifestar convicções de forma respeitosa.', 'NÃO'),
        ('Convicções e Valores', 'CONV05', 'Crenças diversas são respeitadas sem imposição.', 'NÃO'),
        ('Convicções e Valores', 'CONV06', 'Conflitos de valores são evitados ou ignorados.', 'SIM'),
        ('Convicções e Valores', 'CONV07', 'Práticas antiéticas são normalizadas no cotidiano.', 'SIM'),
        ('Convicções e Valores', 'CONV08', 'Há incentivo a ações de responsabilidade social.', 'NÃO'),
        ('Liderança', 'LID01', 'A liderança é acessível e presente no dia a dia.', 'NÃO'),
        ('Liderança', 'LID02', 'Define e comunica prioridades com clareza.', 'NÃO'),
        ('Liderança', 'LID03', 'Reconhece e dá feedback sobre o desempenho.', 'NÃO'),
        ('Liderança', 'LID04', 'Estimula o desenvolvimento/mentoria da equipe.', 'NÃO'),
        ('Liderança', 'LID05', 'Considera dados e escuta a equipe nas decisões.', 'NÃO'),
        ('Liderança', 'LID06', 'Há microgerenciamento excessivo.', 'SIM'),
        ('Liderança', 'LID07', 'Favoritismo influencia decisões e oportunidades.', 'SIM'),
        ('Liderança', 'LID08', 'Promove colaboração entre áreas/equipes.', 'NÃO'),
    ]
    df = pd.DataFrame(data, columns=["Bloco", "ID", "Item", "Reverso"])
    return df

# --- INICIALIZAÇÃO E FORMULÁRIO DINÂMICO ---
df_itens = carregar_itens()
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}

st.subheader("Questionário")
blocos = df_itens["Bloco"].unique().tolist()
def registrar_resposta(item_id, key):
    st.session_state.respostas[item_id] = st.session_state[key]

for bloco in blocos:
    df_bloco = df_itens[df_itens["Bloco"] == bloco]
    prefixo_bloco = df_bloco['ID'].iloc[0][:3] if not df_bloco.empty else bloco # Ajustado para 3 letras
    
    with st.expander(f"{prefixo_bloco}", expanded=(bloco == blocos[0])):
        for _, row in df_bloco.iterrows():
            item_id = row["ID"]
            label = f'({item_id}) {row["Item"]}' + (' (R)' if row["Reverso"] == 'SIM' else '')
            widget_key = f"radio_{item_id}"
            st.radio(
                label, options=["N/A", 1, 2, 3, 4, 5],
                horizontal=True, key=widget_key,
                on_change=registrar_resposta, args=(item_id, widget_key)
            )
# --- VALIDAÇÃO E BOTÃO DE FINALIZAR (MOVIDO PARA O FINAL) ---
# Calcula o número de respostas válidas (excluindo N/A)
respostas_validas_contadas = 0
if 'respostas' in st.session_state:
    for resposta in st.session_state.respostas.values():
        if resposta is not None and resposta != "N/A":
            respostas_validas_contadas += 1

total_perguntas = len(df_itens)
limite_respostas = total_perguntas / 2

# Determina se o botão deve ser desabilitado
botao_desabilitado = respostas_validas_contadas < limite_respostas

# Exibe aviso se o botão estiver desabilitado
if botao_desabilitado:
    st.warning(f"Responda 50% das perguntas (excluindo 'N/A') para habilitar o envio. ({respostas_validas_contadas}/{total_perguntas} válidas)")

# Botão Finalizar com estado dinâmico (habilitado/desabilitado)
if st.button("Finalizar e Enviar Respostas", type="primary", disabled=botao_desabilitado):
        st.subheader("Enviando Respostas...")

        # --- LÓGICA DE CÁLCULO (mantida internamente) ---
        respostas_list = []
        for index, row in df_itens.iterrows():
            item_id = row['ID']
            resposta_usuario = st.session_state.respostas.get(item_id)
            respostas_list.append({
                "Bloco": row["Bloco"], "Item": row["Item"],
                "Resposta": resposta_usuario, "Reverso": row["Reverso"]
            })
        dfr = pd.DataFrame(respostas_list)
        # --- LÓGICA DE ENVIO PARA GOOGLE SHEETS ---
        with st.spinner("Enviando dados para a planilha..."):
            try:
                timestamp_str = datetime.now().isoformat(timespec="seconds")
                respostas_para_enviar = []
                
                for _, row in dfr.iterrows():
                    respostas_para_enviar.append([
                        timestamp_str,
                        respondente,
                        data,
                        organizacao_coletora,
                        row["Bloco"],
                        row["Item"],
                        row["Resposta"] if pd.notna(row["Resposta"]) else "N/A",
                    ])
                
                ws_respostas.append_rows(respostas_para_enviar, value_input_option='USER_ENTERED')
                
                st.success("Suas respostas foram enviadas com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao enviar dados para a planilha: {e}")

# --- BOTÃO INVISÍVEL PARA PINGER (COM st.empty) ---
with st.empty():
    st.markdown('<div id="autoclick-div">', unsafe_allow_html=True) 
    if st.button("Ping Button", key="autoclick_button"):
        print("Ping button clicked by automation.")
    st.markdown('</div>', unsafe_allow_html=True)