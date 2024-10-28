FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV USE_FIRESTORE_EMULATOR=true
ENV FIRESTORE_EMULATOR_HOST=firestore:8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]