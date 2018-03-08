#!/usr/bin/env bash

export KOPS_STATE_STORE=s3://$1-$2-state
export K8_CLUSTER_NAME=k8.$2.$3

kops export kubecfg $K8_CLUSTER_NAME

retries=22
until kops validate cluster $K8_CLUSTER_NAME
do
  if (( retries-- == 0)) ;
    then exit 1;
    else printf "\nCluster not up; Checking again in 15 seconds..\n" && sleep 15;
  fi
done