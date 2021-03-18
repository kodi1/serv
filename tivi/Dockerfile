FROM python:3.11-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN TMP=/docker_temp &&  \
  DST=./ && \
  mkdir -p $TMP && \
  mkdir -p $DST && \
  wget -O $DST/mapping.py https://raw.githubusercontent.com/harrygg/plugin.program.tvbgpvr.backend/master/resources/lib/mapping.py && \
  wget -O $TMP/master.tar.gz https://github.com/kodi1/hts.tivi.bridge/archive/master.tar.gz && \
  tar xf $TMP/master.tar.gz -C $TMP --strip-components=1 && \
  cp $TMP/main.py $DST && \
  cp $TMP/server.py $DST && \
  cp $TMP/tivi.py $DST && \
  cp $TMP/requirements.txt $DST && \
  ls -al $DST && \
  rm -rf $TMP

RUN pip install --no-cache-dir -r requirements.txt

ENV TIVIBG_MAC aa:bb:cc:dd:ee:ff

EXPOSE 8888

CMD [ "python", "./main.py"]
