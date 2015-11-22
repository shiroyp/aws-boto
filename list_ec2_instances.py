#!/usr/bin/env python3
import boto3

# client = boto3.client('ec2', region_name='eu-west-1')

def list_aws_regions():
    """this function will return a list of aws region codes"""
    region = []
    client = boto3.client('ec2', region_name='us-east-1')
    desc_regions = client.describe_regions()
    regions_list = desc_regions['Regions']
    for regions in regions_list:
        region.append(regions['RegionName'])
    return region

def list_instances(region):
    print(region)
    client = boto3.resource('ec2', region)
    # desc_tags = client.describe_tags()
    # tags = desc_tags['Tags']
    # for i in range(0,len(tags)):
    #     each_tag = tags[i]
    #     if (each_tag['ResourceType'] == 'instance' and each_tag['Key'] == 'Name'):
    #         print (each_tag['ResourceId'] + ' - ' + each_tag['Value'] )

    instances = client.instances.all()
    for each in instances:
        print(each.instance_id + '\t' + each.state['Name'] + '\t' + each.instance_type + '\t' + each.private_ip_address + '\t' + str(each.public_ip_address) + '\t' + str(each.key_name))
    print('====================================')

    # Printing only running instance information
    # instances = client.instances.filter(Filters=[
    #     {
    #         'Name': 'instance-state-name',
    #         'Values': [
    #             'running'
    #         ]
    #     }
    # ])
    # for each in instances:
    #     print (each.id + '\t' + each.state['Name'])

# print (list_aws_regions())

for region in list_aws_regions():
    list_instances(region)


