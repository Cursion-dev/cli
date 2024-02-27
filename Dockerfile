FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1

# create the app user
RUN addgroup -S app && adduser -S app -G app

# installing scanerr
RUN pip install scanerr

