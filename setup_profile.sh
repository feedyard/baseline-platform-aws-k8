#!/usr/bin/env bash
mkdir ~/.aws

cat <<EOF > ~/.aws/credentials
[default]
aws_access_key_id=$1
aws_secret_access_key=$2
region=us-east-1
EOF