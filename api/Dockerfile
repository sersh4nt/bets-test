# builder

FROM python:3.9.6-alpine as builder

WORKDIR /usr/app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev


COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/app/src/wheels -r requirements.txt


# run

FROM python:3.9.6-alpine

RUN mkdir -p /home/app && addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/app/src/wheels /wheels
COPY --from=builder /usr/app/src/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

COPY . $APP_HOME

RUN mkdir -p static && python manage.py collectstatic --noinput

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
