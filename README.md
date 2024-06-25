
# Ansible Role:  `telegraf`

Ansible role to install and configure [telegraf](https://www.influxdata.com/time-series-platform/telegraf/).

> Telegraf is a server-based agent for collecting and sending all metrics and events from databases, systems, 
> and IoT sensors.
>
> Telegraf is written in Go and compiles into a single binary with no external dependencies, and requires a very 
> minimal memory footprint.


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-telegraf/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-telegraf)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-telegraf)][releases]
[![Ansible Downloads](https://img.shields.io/ansible/role/d/bodsch/telegraf?logo=ansible)][galaxy]

[ci]: https://github.com/bodsch/ansible-telegraf/actions
[issues]: https://github.com/bodsch/ansible-telegraf/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-telegraf/releases
[galaxy]: https://galaxy.ansible.com/ui/standalone/roles/bodsch/telegraf/


If `latest` is set for `telegraf_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/bin/telegraf/${telegraf_version}` and later linked to `/usr/bin`.  
This should make it possible to downgrade relatively safely.

The telegraf archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`.  
By default it is `${HOME}/.cache/ansible/telegraf`.  
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `telegraf_direct_download` to `true`.


## Operating systems

Tested on

* Arch Linux
* Artix Linux
* Debian based
    - Debian 10 / 11 / 12
    - Ubuntu 20.10 / 22.04

> **RedHat-based systems are no longer officially supported! May work, but does not have to.**


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-telegraf/tags)!

## Configuration

```yaml
telegraf_version: 1.25.0

telegraf_release_download_url: https://dl.influxdata.com/telegraf/releases

telegraf_system_user: telegraf
telegraf_system_group: telegraf
telegraf_config_dir: /etc/telegraf
telegraf_data_dir: /var/lib/telegraf

telegraf_enable_experimental: false

telegraf_direct_download: false

telegraf_service: {}

telegraf_config_agent: {}
telegraf_config_outputs: []
telegraf_config_inputs: []
telegraf_config_processors: []
telegraf_config_aggregators: []
```

### `telegraf_service`

```yaml
telegraf_service:
  config:
    file: "{{ telegraf_config_dir }}/telegraf.conf"
    directory: "{{ telegraf_config_dir }}/telegraf.d"
  pprof_addr: ""    # e.g. 'localhost:6060'
  watch_config: "notify"  # notify, poll
  pidfile: ""
  once: false
  debug: false
  quiet: false
  raw_flags: {}
```

### `telegraf_config_agent`

For more options, please read the [official documentation](https://docs.influxdata.com/telegraf/v1.26/configuration/#agent-configuration).


```yaml
telegraf_config_agent:
  interval: "10s"
  round_interval: true
  metric_batch_size: 1000
  metric_buffer_limit: 10000
  collection_jitter: "0s"
  collection_offset: "0s"
  flush_interval: "10s"
  flush_jitter: "0s"
  precision: "0s"
  debug: false
  quiet: false
  logtarget: "file"
  logfile: "/var/log/telegraf.log"
  logfile_rotation_interval: "" # "0h"
  logfile_rotation_max_size: "0MB"
  logfile_rotation_max_archives: 5
  log_with_timezone: ""
  hostname: ""
  omit_hostname: false
  snmp_translator: "netsnmp"
```

### `telegraf_config_outputs`

For more options and plugins, please read the [official documentation](https://docs.influxdata.com/telegraf/v1.26/plugins/#output-plugins).

**Example with plugins**:

```yaml
telegraf_config_outputs:
  - type: influxdb_v2
    config:
      urls: []
      #  - "http://127.0.0.1:8086"
      token: ""
      organization: ""
      bucket: ""
      bucket_tag: ""
      exclude_bucket_tag: false
      timeout: "5s"
      http_headers: {"X-Special-Header": "Special-Value"}
      http_proxy: "http://corporate.proxy:3128"
      user_agent: "telegraf"
      content_encoding: "gzip"
      influx_uint_support: false
      tls:
        ca: ""    # "/etc/telegraf/ca.pem"
        cert: ""  # "/etc/telegraf/cert.pem"
        key: ""   # "/etc/telegraf/key.pem"
        insecure_skip_verify: false
  - type: influxdb
    config:
      urls:
        - "http://influx1:8089"
```

currently not testet output plugins:

- amon
- amqp
- application_insights
- azure_data_explorer
- azure_monitor
- bigquery
- cloud_pubsub
- cloudwatch
- cloudwatch_logs
- cratedb
- datadog
- discard
- dynatrace
- elasticsearch
- event_hubs
- exec
- execd
- file
- graphite
- graylog
- groundwork
- health
- http
- instrumental
- iotdb
- kafka
- kinesis
- librato
- logzio
- loki
- mongodb
- mqtt
- nats
- newrelic
- nsq
- opentelemetry
- opentsdb
- postgresql
- prometheus_client
- riemann
- riemann_legacy
- sensu
- signalfx
- socket_writer
- sql
- stackdriver
- stomp
- sumologic
- syslog
- timestream
- warp10
- wavefront
- websocket
- yandex_cloud_monitoring


### `telegraf_config_inputs`

For more options and plugins, please read the [official documentation](https://docs.influxdata.com/telegraf/v1.26/plugins/#input-plugins).

**Example with plugins**:

```yaml
telegraf_config_inputs:
  - plugin: cpu
    config:
      percpu: "true"
      totalcpu: true
    tags:
      foo: bar
      bar: foo
    tagdrop:
      bar:
        - foo

  - plugin: disk
    config:
      mount_points:
        - "/"
      ignore_fs: ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]
      ignore_mount_opts: []
  - plugin: io
  - plugin: mem
  - plugin: net
  - plugin: system
  - plugin: swap
  - plugin: netstat
  - plugin: processes
  - plugin: kernel
  - plugin: cgroup
    config:
      paths:
        - "/sys/fs/cgroup/memory"
        - "/sys/fs/cgroup/memory/child1"
        - "/sys/fs/cgroup/memory/child2/*"
      files: ["memory.*usage*", "memory.limit_in_bytes"]
```

### `telegraf_config_processors`

For more options and plugins, please read the [official documentation](https://docs.influxdata.com/telegraf/v1.26/plugins/#processor-plugins).

**Example with plugins**:

```yaml
telegraf_config_processors:
  - processor: rename
  - processor: rename.replace
    config:
      tag: "level"
      dest: "LogLevel"
```

### `telegraf_config_aggregators`

For more options and plugins, please read the [official documentation](https://docs.influxdata.com/telegraf/v1.26/plugins/#aggregator-plugins).

**Example with plugins**:

```yaml
telegraf_config_aggregators:
  - aggregator: basicstats
    config:
      drop_original: false
      stats: ['mean']
    tagpass:
      cpu: ["cpu-total"]
```


## Author

- Bodo Schulz

## License

This project is licensed under Apache License. See [LICENSE](/LICENSE) for more details.

**FREE SOFTWARE, HELL YEAH!**
