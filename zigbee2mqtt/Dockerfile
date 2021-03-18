ARG version

FROM koenkk/zigbee2mqtt:${version}
MAINTAINER kodi1 version: 0.1

RUN \
	sed -i -e "s|^.*_TZE200_py4cm3he.*$|&\n'_TZE200_kly8gjlz',|g" /app/node_modules/zigbee-herdsman-converters/devices/tuya.js
