#!/bin/bash -eux

curl http://localhost:8080/health --retry 30 --retry-delay 1 --retry-max-time 60 --retry-all-errors
