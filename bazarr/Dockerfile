ARG version

FROM linuxserver/bazarr:${version}

COPY . /usr/bin

#RUN sed -i -e 's:minutes=\([[:digit:]]\+\):minutes=30:g' /app/bazarr/scheduler.py

RUN \
        apk update --no-cache && \
        apk add --no-cache py3-pip python3-dev ffmpeg4-dev git libtool autoconf automake musl-dev bison make linux-headers g++ && \
        mkdir -p /tmp/delme && cd /tmp/delme && \
        wget https://dl-cdn.alpinelinux.org/alpine/v3.18/main/x86_64/swig-4.1.1-r4.apk && \
        apk add swig-4.1.1-r4.apk && \
        git clone https://github.com/cmusphinx/sphinxbase.git && \
        git clone https://github.com/cmusphinx/pocketsphinx.git && \
        git clone https://github.com/sc0ty/subsync.git && \
        cd sphinxbase && ./autogen.sh && make install && cd - && \
        cd pocketsphinx && git checkout --detach last-pre-1.0 && ./autogen.sh && make install && cd - && \
        cd subsync && \
        git checkout --detach 0.17 && \
        sed "/configpath = os.path.join/i configdir = os.path.join('/config', appname)\nshareddir = configdir" subsync/config.py.template > subsync/config.py && \
        sed -i -e 's|^.*\#include <string>.*$|&\n\#include <cstdint>|g' gizmo/text/utf8.h && \
        sed -i -e 's|^.*\#include <string>.*$|&\n\#include <cstdint>|g' gizmo/text/ssa.h && \
        pip3 install . && \
        cd / && rm -rf /tmp/delme && \
        apk del python3-dev git libtool autoconf automake musl-dev bison make linux-headers g++ && \
        sed -i -e 's:time.sleep.*$:time.sleep(30.0):g' /app/bazarr/bin/bazarr.py && \
        sed -i -e 's:rows\[\:25\]:rows:g' /app/bazarr/bin/custom_libs/subliminal_patch/providers/yavkanet.py
