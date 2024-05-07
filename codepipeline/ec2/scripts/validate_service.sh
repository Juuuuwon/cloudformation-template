#!/bin/bash -eux

curl --silent http://localhost:8080/health --retry 30 --retry-delay 1 --retry-max-time 60 --retry-all-errors
