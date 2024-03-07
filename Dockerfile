FROM python:3.11
#COPY requirements.txt /app/requirements.txt


# Install basics
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y git make wget curl bison vim fish pandoc

# Install Google Chrome (needed for selenium)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN google-chrome --version


COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN cd /app && poetry install