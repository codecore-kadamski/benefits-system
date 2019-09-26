FROM python:3.7

RUN apt-get update && apt-get install --yes binutils libpq-dev

# install poetry (versions should be updated manually)
#RUN pip install pip==19.1.1 poetry==0.12.16 && poetry config settings.virtualenvs.create false
RUN pip install --upgrade pip
RUN pip install poetry==0.11.5 && poetry config settings.virtualenvs.create false

# create application directory
RUN mkdir -p /app
WORKDIR /app

# copy project requirements files
COPY auths_domain/pyproject.toml .

# install dependencies:
RUN poetry install -n --no-dev

ENV PYTHONPATH=/app/
ENV FLASK_APP=.
ENV ENVIRON=prod

COPY auths_domain/ .

EXPOSE 5000
