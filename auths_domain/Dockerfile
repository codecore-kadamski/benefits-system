FROM python:3.7-slim

RUN apt-get update && apt-get install --yes binutils libpq-dev python3-psycopg2 python3-dev gcc

RUN pip install --upgrade pip

RUN pip install poetry==0.11.5 && poetry config settings.virtualenvs.create false

#ADD . /

RUN mkdir -p /app
WORKDIR /app
COPY pyproject.toml .
COPY ./ .

RUN poetry install -n --no-dev

ENV PYTHONPATH=/app/
ENV FLASK_APP=.
ENV ENVIRON=prod

EXPOSE 5000

CMD ["gunicorn", "wsgi:application", "-w", "2", "-b", "0.0.0.0:5000", "--capture-output", "--access-logfile", "-", "--access-logformat", "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" \"%(s)\" %(b)s \"%(f)s\" \"%(a)s\" \"%({x-client}i)s\" \"%({Host}i)s\" \"%(L)s\" X-Mobile-Agent: \"%({x-mobile-agent}i)s\""]
