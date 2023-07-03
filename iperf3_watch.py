#!/usr/bin/env python

import argparse
import re
import subprocess
import sys

DEFAULT_THRESHOLD_BYTES = 100000

BYTES_REGEX = re.compile('.*\s+sec\s+([\d\.]+\s+\w+)\s+')

parser = argparse.ArgumentParser()
parser.add_argument('--report-threshold', default=DEFAULT_THRESHOLD_BYTES)
FLAGS, iperf_args = parser.parse_known_args()


def iperf_xfer_bytes(line: str) -> float:
    match = BYTES_REGEX.match(line)
    if not match:
        return 0.0
    xfer_data = match.groups()[0]
    xfer_bytes = xfer_data_bytes(xfer_data)
    return xfer_bytes


def xfer_data_bytes(xfer_data: str) -> float:
    xfer_count_str, xfer_suffix = xfer_data.split()
    xfer_count = float(xfer_count_str)
    xfer_bytes = 0
    if xfer_suffix[0] == "B":
        return xfer_count
    elif xfer_suffix[0] == "K":
        return xfer_count * 1024
    elif xfer_suffix[0] == "M":
        return xfer_count * 1024 * 1024


def main():
    iperf_argv = ["iperf3", "--forceflush"] + iperf_args
    #print("executing", iperf_argv)

    threshold_bytes = float(FLAGS.report_threshold)

    with subprocess.Popen(iperf_argv, stdout=subprocess.PIPE) as proc:
        accum_bytes = 0
        while True:
            stdout_data = proc.stdout.readline()
            line = stdout_data.decode().rstrip()
            if line:
                #print("iperf output:", line)
                xfer_bytes = iperf_xfer_bytes(line)
                #print("transferred", xfer_bytes)
                accum_bytes += xfer_bytes
                if accum_bytes >= threshold_bytes:
                    print("threshold", threshold_bytes, "reached")
                    sys.stdout.flush()
                    accum_bytes -= threshold_bytes
            proc.poll()
            if proc.returncode is not None:
                break


if __name__ == "__main__":
    main()
