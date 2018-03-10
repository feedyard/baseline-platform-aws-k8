#!/usr/bin/env bash

export KOPS_STATE_STORE=s3://$1-$2-state
export K8_CLUSTER_NAME=k8.$2.$3

if [[ ! $(kops get cluster --name $K8_CLUSTER_NAME) ]]; then
    kops create -f $2_cluster.yml
    kops create secret --name $K8_CLUSTER_NAME sshpublickey admin -i $2.id_rsa.pub
else
    kops replace -f $2_cluster.yml
fi

kops update cluster $K8_CLUSTER_NAME --yes
