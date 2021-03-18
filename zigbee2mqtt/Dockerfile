ARG version

FROM koenkk/zigbee2mqtt:${version}

COPY kly8gjlz.patch /app

RUN apk add patch \
	&& patch /app/node_modules/.pnpm/*/node_modules/zigbee-herdsman-converters/dist/devices/tuya.js /app/kly8gjlz.patch
