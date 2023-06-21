#!/bin/bash -eux

pip3 install -r /opt/app/requirements.txt

if [ -d /opt/app/__pycache__ ]
then
    rm -rf /opt/app/__pycache__
fi

if [ -e /opt/app/app.service ]
then
    cp /opt/app/app.service /etc/systemd/system/app.service
    systemctl daemon-reload
fi
