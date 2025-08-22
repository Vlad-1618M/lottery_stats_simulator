FROM alpine:latest

WORKDIR /side_monitor

# ... oopy all just to be safe: 
COPY build/gotools/go_compiled /tmp/go_binaries

# ... find the latest linux amd64 binary to copy:
RUN latest_dir=$(find /tmp/go_binaries -type d -name '*amd64' | sort | tail -n1) && \
    cp "$latest_dir/go_watcher" /side_monitor/go_watcher && \
    chmod +x /side_monitor/go_watcher

COPY build/gotools/cfg.yml /side_monitor/cfg.yml

CMD ["./go_watcher"]

# # docker build -t sidecar --progress=plain -f build/sidecar/monitor.Dockerfile .