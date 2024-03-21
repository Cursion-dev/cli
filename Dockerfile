FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1

LABEL Author="Scanerr" Support="hello@scanerr.io"

# create the app user
RUN addgroup --system app && adduser --system app 

# installing python3 & pip
RUN apt-get update && apt-get install -y python3 python3-pip

# installing scanerr & deps
RUN python3 -m pip install scanerr==0.0.6 typer requests rich python-dotenv

# entry point
ENTRYPOINT [ "scanerr" ]