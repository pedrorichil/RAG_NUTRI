import streamlit as st
import requests as rq
from time import sleep
from json import loads, dumps
import os
import pandas as pd

# Configuração da página
st.set_page_config(page_title="FAQ - Nutri - Mrx")

# Caminho fixo para armazenar mensagens
SESSIONS_DIR = os.path.expanduser("~/sessions")
SESSION_FILE = f"{SESSIONS_DIR}/chat_history.json"

# Criar diretório para sessões se não existir
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

# Carregar mensagens salvas anteriormente
if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "r") as f:
        try:
            st.session_state.messages = loads(f.read())
        except:
            st.session_state.messages = []
else:
    st.session_state.messages = []

# Limita o histórico a 4 mensagens
st.session_state.messages = st.session_state.messages[-4:]

# Função para salvar mensagens
def save_messages(messages):
    with open(SESSION_FILE, "w") as f:
        f.write(dumps(messages[-4:]))  # Salva apenas as últimas 4 mensagens

# Função para converter entrada para string
def format_input(input_value):
    if isinstance(input_value, str):
        return input_value
    elif isinstance(input_value, dict):
        return dumps(input_value, indent=2)
    elif isinstance(input_value, pd.DataFrame):
        return input_value.dropna(how="all").to_markdown(index=False)
    else:
        return str(input_value)

# Função para exibir mensagens com configuração personalizada
def display_message(role, content, sender_name="User", background_color="#E8E8E8", text_color="#000000", icon="💬"):
    with st.chat_message(role, avatar=icon):
        st.markdown(f"<span style='color:{text_color}; font-weight:bold;'>{sender_name}:</span> {content}", unsafe_allow_html=True)

st.title("FAQ - Nutrição - AI")

# Função para simular a escrita do chatbot
def stream_data(data: str):
    for word in data.split(" "):
        yield word + " "
        sleep(0.1)

# Exibir as últimas 2 mensagens armazenadas
for message in st.session_state.messages[-2:]:
    display_message(
        message["role"],
        message["content"],
        sender_name=message.get("sender_name", "User"),
        background_color=message.get("background_color", "#E8E8E8"),
        text_color=message.get("text_color", "#000000"),
        icon=message.get("icon", "💬")
    )

# Captura entrada do usuário
user_input = st.chat_input("Qual é a sua dúvida?")

if user_input:
    formatted_input = format_input(user_input)
    display_message("user", formatted_input, sender_name="Você", icon="👤")

    # Envia a requisição para a API
    response = rq.post(
        "https://langflow.quickfix-dev-pbrito.shop/api/v1/run/bf149992-3e8c-4e95-b469-d3288bc0e4eb?stream=false",
        json={
            "input_value": formatted_input,
            "output_type": "chat",
            "input_type": "chat"
        }
    )

    if response.status_code == 200:
        try:
            data = response.json()
            ai_response = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
        except (KeyError, IndexError, TypeError):
            ai_response = "Erro ao processar resposta da IA."
    else:
        ai_response = "Erro ao conectar-se à API."

    display_message("ai", ai_response, sender_name="Mrx IA", background_color="#D3E3FC", text_color="#003366", icon="🤖")

    # Atualiza o histórico de mensagens
    st.session_state.messages.append({
        "role": "user", "content": formatted_input, "sender_name": "Você", "icon": "👤"
    })
    st.session_state.messages.append({
        "role": "ai", "content": ai_response, "sender_name": "Mrx IA", "background_color": "#D3E3FC", "text_color": "#003366", "icon": "🤖"
    })

    # Salva no arquivo JSON
    save_messages(st.session_state.messages)
