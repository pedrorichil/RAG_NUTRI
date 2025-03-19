# Base image
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Instalação de dependências mínimas e nano
RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    curl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Argumentos para autenticação Git
ARG GIT_USER
ARG GIT_PASSWORD

# Clone do repositório com autenticação
RUN git clone http://pbrito:Bianeves189.@192.168.22.29:3003/pbrito/FAQ-IRPF-Krypton.git .

# Instalação de dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretório persistente
RUN mkdir -p /app/sessions && chmod -R 777 /app/sessions

# Definir volume para persistência de sessões
VOLUME /app/sessions

# Expor a porta do Streamlit
EXPOSE 8501

# Entrada principal do container
CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]