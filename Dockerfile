FROM python:3.10-slim

WORKDIR /app

# Installazione dipendenze di sistema necessarie per ChromaDB e PDF
RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia i requisiti
COPY requirements.txt .

# Forza l'aggiornamento di pip e l'installazione dei pacchetti
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir streamlit 

# Copia il resto dei file
COPY . .

EXPOSE 8501

# Avvio tramite modulo python
ENTRYPOINT ["python", "-m", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]