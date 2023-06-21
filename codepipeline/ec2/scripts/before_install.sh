#!/bin/bash -eux

if systemctl list-units | grep app.service
then
    systemctl disable --now app.service
fi
