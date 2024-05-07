#!/bin/bash -eux

# If app.service exists, disable and stop it
if systemctl list-units | grep app.service
then
    systemctl disable --now app.service
fi

# If venv does not exist
if [ ! -d /opt/app/venv ]
then
    python3 -m ensurepip
    python3 -m pip install virtualenv
    python3 -m virtualenv /opt/app/venv
fi

# Install python packages
/opt/app/venv/bin/pip3 install -r /opt/app/requirements.txt

# Delete application __pycache__
if [ -d /opt/app/__pycache__ ]
then
    rm -rf /opt/app/__pycache__
fi

# Overwrite app.service
if [ -e /opt/app/app.service ]
then
    cp /opt/app/app.service /etc/systemd/system/app.service
    systemctl daemon-reload
fi
