FROM python:3.11 

WORKDIR /app 

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt 
RUN  pip install "cloud-sql-python-connector[pg8000]"

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]