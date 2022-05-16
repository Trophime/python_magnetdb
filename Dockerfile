FROM trophime/magnetdb

RUN apt-get update
RUN apt-get install -y curl wget libpq-dev build-essential python3-minimal libpython3.8-dev python3-pip
RUN python -m pip install --upgrade pip

USER vscode

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
