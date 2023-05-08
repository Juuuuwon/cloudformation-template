#!/bin/bash
if [ ! -d /opt/app ]; then
    mkdir -p /opt/app
fi

if [ ! -f /usr/bin/pypy3 ]; then
    wget https://downloads.python.org/pypy/pypy3.9-v7.3.11-linux64.tar.bz2 -P /tmp/
    tar xf /tmp/pypy3.9-v7.3.11-linux64.tar.bz2 -C /tmp/
    ln -s /tmp/pypy3.9-v7.3.11-linux64/bin/pypy3 /usr/bin/pypy3
    pypy3 -m ensurepip
fi
