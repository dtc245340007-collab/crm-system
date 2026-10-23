FROM python:3.11-slim
RUN groupadd -r crmuser && useradd -r -g crmuser crmuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chown -R crmuser:crmuser /app
USER crmuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
