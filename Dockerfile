# Usa una versione leggera di Python
FROM python:3.10-slim

# Crea una cartella di lavoro
WORKDIR /app

# Copia i requisiti e installali
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto (il tuo main.py e i documenti)
COPY . .

# Comando per avviare il bot in modalità interattiva
CMD ["python", "main.py"]