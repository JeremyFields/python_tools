#!/usr/bin/python
# Author     : Jeremy Fields
# Description: This script enables or disables termination protection of EC2 instances.
### # # # # # # # # # # # # # # # # # # USAGE # # # # # # # # # # # # # # # # # # # ###
# Syntax: 
#   python disable_term_protection.py --instance cluster1 cluster2 cluster3... --disable
#   python disable_term_protection.py --instance cluster1 cluster2 cluster3... --enable
# Args:
#   --instance : the clusters you want to enable / disable term protection on.
#   --disable  : flag to disable termination protection
#   --enable   : flag to enable termination protection

import boto3
import argparse

''' Args '''
parser = argparse.ArgumentParser()
parser.add_argument("--instance", nargs="*", help="zookeeper-scale-dev")
parser.add_argument("--disable", action="store_false")
parser.add_argument("--enable", action="store_true")
args = parser.parse_args()

instances = args.instance
instance_ids = []
client = boto3.client('ec2')

for instance in instances:
    responses = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [instance]
            }
        ]
    )
    
    for response in responses['Reservations']:
        for instance in response['Instances']:
            instance_ids.append(instance['InstanceId'])

if args.disable == False:
    for id in instance_ids:
        id = ''.join(id)
        modifier = client.modify_instance_attribute(
            DisableApiTermination={'Value': args.disable},
            InstanceId=id
        )
elif args.enable == True:
    for id in instance_ids:
        id = ''.join(id)
        modifier = client.modify_instance_attribute(
            DisableApiTermination={'Value': args.enable},
            InstanceId=id
        )