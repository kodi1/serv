FROM python:2

MAINTAINER kodi1 version: 0.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN TMP=/docker_temp &&  \
  DST=./ && \
  mkdir -p $TMP && \
  mkdir -p $DST && \
  wget -O $TMP/bgtv.tar.gz https://github.com/kodi1/hts.bgtv.bridge/archive/master.tar.gz && \
  tar xf $TMP/bgtv.tar.gz -C $TMP --strip-components=1 && \
  cp $TMP/*.py $DST && \
  cp $TMP/chmap.json $DST && \
  cp $TMP/data.dat $DST && \
  cp $TMP/requirements.txt $DST && \
  ls -al $DST && \
  rm -rf $TMP

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV KEY 0123456789abcdef

EXPOSE 8888

CMD [ "python", "./main.py"]
