FROM python:3.9.2-slim-buster

WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && rm -rf ~/.cache

CMD ["python", "src/bot.py"]