ARG version

FROM linuxserver/bazarr:${version}
COPY . /usr/bin

RUN sed -i -e 's:time.sleep.*$:time.sleep(30.0):g' /app/bazarr/bin/bazarr.py && \
    sed -i -e 's:rows\[\:25\]:rows:g' /app/bazarr/bin/custom_libs/subliminal_patch/providers/yavkanet.py
