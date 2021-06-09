#!/bin/bash

docker ps -a --format "{{.Names}}  {{.Status}}" | grep Up | awk '{print $1}' | sort
