FROM python:3.8.5-slim

WORKDIR /usr/home

COPY ./requirements.txt .
 
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]