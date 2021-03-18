#docker build --build-arg _UID=$(id -u) --build-arg _GID=$(id -g) -t daikin .
#docker run --rm -it --network=host -v $PWD/app:/work/app daikin bash
FROM ubuntu:22.04

ARG _UID
ARG _GID

ARG _WRK=/work

ENV HOME=${_WRK}
ENV TZ=Europe/Sofia

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    curl \
    wget \
    sudo \
    ssh \
    git \
    unzip \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${_WRK}

ADD app.py .

RUN mkdir -p ${_WRK} && \
    mkdir -p /home/sss && \
    groupadd -g ${_GID} appuser && \
    useradd -r -d ${_WRK} -u ${_UID} -s /bin/bash -g appuser appuser && \
    chown -R ${_UID}:${_GID} ${_WRK} && \
    echo 'appuser ALL=(ALL) NOPASSWD:SETENV: ALL' >> /etc/sudoers && \
    echo 'StrictHostKeyChecking no' >> /etc/ssh/ssh_config && \
    echo '. /etc/bash_completion' >>  /etc/bash.bashrc && \
    echo 'export PATH=/work/tools/bin:$PATH' >> /etc/bash.bashrc

USER appuser

RUN git clone --branch V1.2-work https://github.com/william-sy/Daikin-BRP069A62.git \
    && cd Daikin-BRP069A62 \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir PyYAML \
    && pip install --no-cache-dir paho-mqtt==1.6.1 \
    && pip install --no-cache-dir --force-reinstall websocket-client \
    && ln -s README.MD README.md \
    && pip3 install . \
    && cd - \
    && rm -rf Daikin-BRP069A62

CMD [ "python3", "app.py"]
