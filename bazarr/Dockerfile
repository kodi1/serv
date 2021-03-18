ARG version

FROM linuxserver/bazarr:${version}
MAINTAINER kodi1 version: 0.1

COPY . /usr/bin

#RUN sed -i -e 's:minutes=\([[:digit:]]\+\):minutes=30:g' /app/bazarr/scheduler.py

RUN \
        apk update --no-cache && \
        apk add --no-cache py3-pip python3-dev swig ffmpeg-dev git libtool autoconf automake musl-dev bison make linux-headers g++ && \
        mkdir -p /tmp/delme && cd /tmp/delme && \
        git clone https://github.com/cmusphinx/sphinxbase.git && \
        git clone https://github.com/cmusphinx/pocketsphinx.git && \
        git clone https://github.com/sc0ty/subsync.git && \
        cd sphinxbase && ./autogen.sh && make install && cd - && \
        cd pocketsphinx && ./autogen.sh && make install && cd - && \
        cd subsync && \
        git checkout --detach 0.16 && \
        sed "/configpath = os.path.join/i configdir = os.path.join('/config', appname)\nshareddir = configdir" subsync/config.py.template > subsync/config.py && \
        pip3 install . && \
        cd / && rm -rf /tmp/delme && \
        apk del python3-dev swig ffmpeg-dev git libtool autoconf automake musl-dev bison make linux-headers g++ && \
        sed -i -e 's:time.sleep.*$:time.sleep(30.0):g' /app/bazarr/bin/bazarr.py && \
        sed -i -e 's:weeks=3:weeks=23:g' /app/bazarr/bin/bazarr/get_subtitle.py && \
        sed -i -e 's:weeks=1:days=3:g' /app/bazarr/bin/bazarr/get_subtitle.py
