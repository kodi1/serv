ARG version

FROM koenkk/zigbee2mqtt:${version}

RUN \
	sed -i -e "s|^.*_TZE200_py4cm3he.*$|&\n'_TZE200_kly8gjlz',|g" \
	/app/node_modules/.pnpm/zigbee-herdsman-converters*/node_modules/zigbee-herdsman-converters/dist/devices/tuya.js
