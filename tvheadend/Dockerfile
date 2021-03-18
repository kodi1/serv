ARG version
FROM linuxserver/tvheadend:${version}

RUN apk add  --progress --no-cache \
      py3-paho-mqtt

COPY . /usr/bin
