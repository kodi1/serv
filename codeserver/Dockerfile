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
    pip \
    && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
    && \
    pip3 install --no-cache-dir --break-system-packages \
        click homeassistant-cli \
        yamllint \
    && \
    apt-get purge -y --auto-remove build-essential python3-dev pip \
    && \
    find /usr/local/lib/python3.*/ -depth -type d -name tests -exec rm -rf {} \; \
    && \
    find /usr/local/lib/python3.*/ -depth -type d -name test -exec rm -rf {} \; \
    && \
    find /usr/local/lib/python3.*/ -depth -name __pycache__ -exec rm -rf {} \; \
    && \
    find /usr/local/lib/python3.*/ -depth  -name "*.pyc" -exec rm -f {} \; \
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
    sed -i -e 's:^.*bin/code-server.*$:&\n --cert \\:g' /etc/s6-overlay/s6-rc.d/svc-code-server/run
