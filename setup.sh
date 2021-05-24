#!/usr/bin/env bash
#
# Written for Raspberry Pi OS, you might need to customize this for others
#
# Read the README.md instructions!
#

export PATH=$PATH:~/.local/bin

# Detect latest Python and pip
PIP=$(which pip3.9)
if [[ -z "$PIP" ]]; then
  PIP=$(which pip3.8)
fi
if [[ -z "$PIP" ]]; then
  PIP=$(which pip3.7)
fi
if [[ -z "$PIP" ]]; then
  PIP=$(which pip3.6)
fi
if [[ -z "$PIP" ]]; then
  PIP=$(which pip3)
fi
if [[ -z "$PIP" ]]; then
  PIP=$(which pip)
fi

PYTHON=$(which python3.9)
if [[ -z "$PYTHON" ]]; then
  PYTHON=$(which python3.8)
fi
if [[ -z "$PYTHON" ]]; then
  PYTHON=$(which python3.7)
fi
if [[ -z "$PYTHON" ]]; then
  PYTHON=$(which python3.6)
fi
if [[ -z "$PYTHON" ]]; then
  PYTHON=$(which python3)
fi
if [[ -z "$PYTHON" ]]; then
  PYTHON=$(which python)
fi

set -ex

chmod +x *.sh
sudo apt-get install -y ffmpeg

if [[ ! -f "$HOME/.cargo/env" ]]; then
  if ! which rustc; then
    curl https://sh.rustup.rs -sSf | bash -s -- -y
  fi
fi

if [[ -f "$HOME/.cargo/env" ]]; then
  source $HOME/.cargo/env
fi

# Install script dependencies if not yet installed
if [[ ! -d ".venv" ]]; then
  $PIP install virtualenv
  $PYTHON -m virtualenv .venv
fi

set +x
source .venv/bin/activate
set -x
pip install -r requirements.txt

# Set up a service
DIR=$(pwd -P)
SERVICE=$(cat <<EOF
[Unit]
Description=wttr-kiosk
After=network.target

[Service]
ExecStart=$DIR/start.sh
WorkingDirectory=$DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target

EOF
)

echo "$SERVICE" | sudo tee /etc/systemd/system/wttr-kiosk.service

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable wttr-kiosk
sudo systemctl start wttr-kiosk
