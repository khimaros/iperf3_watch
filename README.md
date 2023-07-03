# `IPERF3_WATCH`

`iperf3_watch` invokes iperf3 interactively and monitors its output.

when a specified byte threshold is reached, `iperf3_watch` outputs a single line.

`iperf3_watch` accepts a single argument `--report-threshold=<bytes>` and all other arguments
are passed through to iperf3 unmodified.

this script was built to workaround a [missing feature](https://github.com/esnet/iperf/issues/1538) in iperf3.

for the best performance, it is recommended to invoke with `-i 0.1` which is the highest rate of
reporting output supported by iperf3.

this script can be used from a bash script as follows:

```shell
iperf3_watch.py --report-threshold=10000 -c <host> -i 0.1 -t 0 | while read line; do
    # do something interesting every 10,000 bytes ...
done
```

see the `examples/` directory for a complete example.
