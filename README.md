# agent9

My agent do docker, nginx, cloudflare stuffs

## how to setup (**python >= 3.8**)

config example see `agent9.ini.example`

```bash
mkdir /opt/agent9
```

```bash
cd /opt/agent9
```

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install git+https://github.com/tuana9a/agent9
```

create service file `/etc/systemd/system/agent9d.service`

```ini
[Unit]
Description=agent9 server

[Service]
ExecStart=/opt/agent9/.venv/bin/agent9 --config /opt/agent9/agent9.ini

[Install]
WantedBy=default.target
```

```bash
sudo systemctl daemon-reload
```

(optional)

```bash
sudo systemctl enable agent9
```
