ARG version
FROM linuxserver/tvheadend:${version}

MAINTAINER kodi1 version: 0.1

RUN apk add  --progress --no-cache \
      py3-paho-mqtt

COPY . /usr/bin
