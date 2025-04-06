# Base image
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano curl git \
 && apt-get purge --auto-remove -y \
 && rm -rf /var/lib/apt/lists/*


# Clone do repositório com autenticação
RUN git clone https://github.com/pedrorichil/RAG_NUTRI.git .

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