FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1

LABEL Author="Cursion" Support="hello@cursion.dev"

# create the app user
RUN addgroup --system app && adduser --system app 

# installing python3 & pip
RUN apt-get update && apt-get install -y python3 python3-pip

# installing cursion & deps
RUN python3 -m pip install cursion==0.0.1 typer requests rich python-dotenv

# entry point
ENTRYPOINT [ "cursion" ]