#!/usr/bin/env bash

export HOST=${HOST:-http://172.18.196.216:35357}
export API_NAME=${API_NAME:-'api_identity_v3.conf'}
export LOG_FILE=${LOG_FILE:-'tempest.log.demo'}
export REPORT_FILE=${REPORT_FILE:-'report.log'}

echo $HOST
echo $API_NAME
echo $LOG_FILE

python checklog.py


