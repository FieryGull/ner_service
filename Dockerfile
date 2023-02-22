FROM python:3.8-slim-buster

RUN apt-get update
RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .
ENTRYPOINT ["python3"]
CMD ["app.py"]