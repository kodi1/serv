FROM python:2-alpine

MAINTAINER kodi1 version: 0.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN TMP=/docker_temp &&  \
  DST=./ && \
  mkdir -p $TMP && \
  mkdir -p $DST && \
  wget -O $TMP/bsc.tar.gz https://github.com/kodi1/plugin.program.bscfusion/archive/dev.tar.gz && \
  tar xf $TMP/bsc.tar.gz -C $TMP --strip-components=1 && \
  cp $TMP/dbg.py $DST && \
  cp $TMP/mapch.json $DST && \
  cp $TMP/requirements.txt $DST && \
  cp -r $TMP/resources/ $DST && \
  ls -al $DST && \
  rm -rf $TMP
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV BSCLOGIN user:pass
ENV BSCREFRESH 90

EXPOSE 8888

CMD [ "python", "./dbg.py", "4"]
