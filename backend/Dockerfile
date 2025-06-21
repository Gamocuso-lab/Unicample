# Usar imagem oficial do Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY ./app /app/app
COPY requirements.txt /app

COPY ./app/templates /app/templates

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta da API
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]