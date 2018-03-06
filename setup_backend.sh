#!/usr/bin/env bash

cat <<EOF > backend.conf
key="baseline-platform-aws-resources/state.tfstate"
bucket="feedyard-$1-state"
region="us-east-1"
profile="default"
EOF