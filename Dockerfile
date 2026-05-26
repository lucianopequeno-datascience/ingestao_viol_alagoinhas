# Usa uma imagem oficial do Python, versão enxuta
FROM python:3.10-slim

# Evita que o Python crie arquivos .pyc e obriga o log no terminal (útil para o GCP)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Instala a libmagic1 (necessária para validação de MIME types no PySUS) e limpa o cache do apt
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação
COPY main.py .

# Comando de execução
CMD ["python", "main.py"]