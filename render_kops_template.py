import json as js
import os
from datetime import datetime, tzinfo, timedelta
from jinja2 import Environment, FileSystemLoader
import argparse

class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)


parser = argparse.ArgumentParser(description='generate kops config template')
parser.add_argument('org', type=str, nargs='?', help='org name used for s3 bucket pattern <org>-<env>-state')
parser.add_argument('vpc_env', type=str, nargs='?', help='the cluster env to deploy')
parser.add_argument('k8_version', type=str, nargs='?', help='version of kubernetes to deploy')
parser.add_argument('ami', type=str, nargs='?', help='ami to use')

args = parser.parse_args()
org = args.org
vpc_env = args.vpc_env
k8_version = args.k8_version
ami = args.ami

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH)),
    trim_blocks=False)

DICTIONARY = {}

def addClusterNameToDictionary(clusterName):
    cluster = js.load(open(clusterName))['value']
    DICTIONARY["cluster_name"] = cluster['name']

def addSubnetDefinitionsToDictionary(subnet_group, subnetDefinition):
    subnets = js.load(open(subnetDefinition))['value']

    for i in range(len(subnets['az'])):
        DICTIONARY['{}_subnet_{}_name'.format(subnet_group,i)] = subnets['name'][i]
        DICTIONARY['{}_subnet_{}_cidr'.format(subnet_group,i)] = subnets['cidr'][i]
        DICTIONARY['{}_subnet_{}_az'.format(subnet_group,i)] = subnets['az'][i]

def addInstanceGroupsToDictionary(subnet_group, subnetDefinition):
    subnets = js.load(open(subnetDefinition))['value']

    for i in range(len(subnets['az'])):
        DICTIONARY['{}_instance_{}'.format(subnet_group,i)] = subnets['az'][i]

def addVpcDefinitionsToDictionary(vpcDefinition):
    vpc = js.load(open(vpcDefinition))['value']
    DICTIONARY["vpc_id"] = vpc['id']
    DICTIONARY["vpc_cidr"] = vpc['cidr']

def addNatGatewayDefinitionsToDictionary(natGwDefinitions):
    natgws = js.load(open(subnetDefinition))['value']
    DICTIONARY['nat_gateway_subnets'] = natgws

def isHA(subnetDefinition):
    subnets = js.load(open(subnetDefinition))['value']
    return False if range(len(subnets['az'])) == 1 else True

def renderKopsSpec():

    DICTIONARY['timestamp'] = str(datetime.utcnow().replace(tzinfo=simple_utc()).isoformat()).split('.', 1)[0] + 'Z'
    DICTIONARY['s3_bucket'] = '{}-{}-state'.format(org, vpc_env)
    DICTIONARY['version'] = k8_version
    DICTIONARY['image'] = ami
    addClusterNameToDictionary('k8_cluster_name.json')
    addSubnetDefinitionsToDictionary('master','nat_subnet_objects.json')
    addSubnetDefinitionsToDictionary('nodes','nat_subnet_objects.json')
    addSubnetDefinitionsToDictionary('utility','public_subnet_objects.json')
    addInstanceGroupsToDictionary('master','nat_subnet_objects.json')
    addVpcDefinitionsToDictionary('vpc.json')
    # addNatGatewayDefinitionsToDictionary('natgateway.json')

    if isHA('nat_subnet_objects.json'):
        template = TEMPLATE_ENVIRONMENT.get_template("cluster_ha_template.yml")
    else:
        template = TEMPLATE_ENVIRONMENT.get_template("cluster_template.yml")
    renderedtemplate = template.render(**DICTIONARY)
    print (renderedtemplate)
    #
    # f = open("{}/{}-cluster.yaml".format(vpc_env, vpc_env), 'w')
    # f.write(renderedtemplate)  # python will convert \n to os.linesep
    # f.close()

if __name__ == '__main__':
    renderKopsSpec()
