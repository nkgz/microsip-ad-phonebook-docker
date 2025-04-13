FROM ubuntu:22.04

WORKDIR /app

COPY microsip.py .

RUN \
  apt update && \
  apt -y install \
    build-essential \
    python3-dev \
    libldap2-dev \ 
    libsasl2-dev \
    slapd \
    ldap-utils \
    tox \
    lcov valgrind \
    python3-pip \
    python3-venv && \
  apt clean && \
  rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN \
  python3 -m pip install python-ldap && \
  chmod +x microsip.py

CMD [ "python3", "./microsip.py"]
