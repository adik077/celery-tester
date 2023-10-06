FROM python:3.9
ENV APP_HOME=/home/app/celeryApp
ENV MAIN_CONTENT_HOME=/home/app/celeryApp/main_content
ENV POETRY_VERSION=1.5.1


RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

#poetry
RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml $APP_HOME
RUN poetry export --without-hashes -f requirements.txt | pip install -r /dev/stdin


COPY . $APP_HOME
ENV FLASK_APP=app.py
EXPOSE 5000

WORKDIR $MAIN_CONTENT_HOME
CMD ["python3", "-m" , "flask", "run", "--host", "0.0.0.0", "--port", "5000"]
