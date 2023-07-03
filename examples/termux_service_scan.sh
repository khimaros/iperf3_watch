#!/bin/bash

REPORT_THRESHOLD=100000

SOUND="${HOME}/downloads/service-found.opus"

PYTHON="/data/data/com.termux/files/usr/bin/python3"

SERVER="10.1.200.1"

service_found() {
	termux-media-player play "${SOUND}"
	echo "service found!" >&2
}

iperf3_watch() {
	${PYTHON} ${HOME}/bin/iperf3_watch.py \
		--report-threshold=${REPORT_THRESHOLD} \
		-c "$SERVER" -R -t 0 -i 0.1
}

termux-wake-lock

iperf3_watch | while read line; do
	service_found
done

termux-wake-unlock

read FNORD
