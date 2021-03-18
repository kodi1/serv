ARG BUILD_FROM=linuxserver/code-server

FROM ${BUILD_FROM}

RUN \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3 \
    mosquitto-clients \
    wget \
    colordiff \
    git \
    vim \
    && \
    curl https://bootstrap.pypa.io/get-pip.py | python3 \
    && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
    && \
    pip3 install --no-cache-dir \
        homeassistant_cli \
        yamllint \
    && \
    apt-get purge -y --auto-remove build-essential python3-dev \
    && \
    find /usr/local/lib/python3.6/ -type d -name tests -depth -exec rm -rf {} \; \
    && \
    find /usr/local/lib/python3.6/ -type d -name test -depth -exec rm -rf {} \; \
    && \
    find /usr/local/lib/python3.6/ -name __pycache__ -depth -exec rm -rf {} \; \
    && \
    find /usr/local/lib/python3.6/ -name "*.pyc" -depth -exec rm -f {} \; \
    && \
    rm -frv /tmp/* /var/{cache,log}/* /var/lib/apt/lists/* \
    && \
    printf '\neval "$(hass-cli completion bash)"\n' >> /etc/bash.bashrc \
    && \
    printf "    Protocol 2\n" >> /etc/ssh/ssh_config \
    && \
    printf "    TCPKeepAlive yes\n" >> /etc/ssh/ssh_config \
    && \
    printf "    ServerAliveInterval 300\n" >> /etc/ssh/ssh_config \
    && \
    printf "    StrictHostKeyChecking no\n" >> /etc/ssh/ssh_config \
    && \
    printf "    UserKnownHostsFile /dev/null\n" >> /etc/ssh/ssh_config \
    && \
    sed -i -e 's:^.*code-server.*$:&\n --cert \\:g' /etc/services.d/code-server/run

MAINTAINER kodi1 version: 0.1
