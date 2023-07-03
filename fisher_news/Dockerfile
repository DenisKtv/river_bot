FROM python:3-slim

WORKDIR /app

COPY fisher_news/requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY fisher_news/ /app

CMD ["gunicorn", "fisher_news.wsgi:application", "--bind", "0:8000"]