FROM python:3.7.3

# install GDAL
#RUN apt-get update && apt-get install --yes binutils libproj-dev gdal-bin \
#    && rm -rf /var/lib/apt/lists/*

# install poetry (versions should be updated manually)
RUN pip install pip==19.1.1 poetry==0.12.16 && poetry config settings.virtualenvs.create false

# create application directory
RUN mkdir -p /app
WORKDIR /app

# copy project requirements files
COPY auths_service/pyproject.toml .

# install dependencies:
RUN poetry install -n --no-dev

ARG ENV_MODE=Develop
ENV PYTHONPATH=/app/
ENV FLASK_APP=.

RUN if [ "$ENV_MODE" != "Staging" ] ; then poetry install -n; fi

# get wait-for-it.sh
#ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/54d1f0bfeb6557adf8a3204455389d0901652242/wait-for-it.sh .
#RUN chmod 755 wait-for-it.sh

COPY auths_service/app.py .
COPY auths_service/auth_service auth_service/

EXPOSE 5000
