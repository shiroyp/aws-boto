__author__ = 'shiroyp'

"""
A Sample python program to navigate through your aws security groups in every region and check for security groups which are world wide open for SSH
"""
import boto3

client = boto3.client('ec2', region_name='us-east-1')

desc_regions = client.describe_regions()

for region in desc_regions['Regions']:
    print (region['RegionName'])
    weak_sgs=[]
    new_client=boto3.client('ec2',region_name=region['RegionName'])
    desc_sg = new_client.describe_security_groups()
    # print (desc_sg)
    for sg in desc_sg['SecurityGroups']:
        # print(sg['GroupId'])
        for IpPerms in sg['IpPermissions']:
            if ('FromPort' in IpPerms.keys() and 'ToPort' in IpPerms.keys()):
                if (IpPerms['FromPort'] <= 22 and IpPerms['ToPort'] >= 22):
                    # print(sg['GroupId'] + ' ' + str(IpPerms['FromPort']) + ' - ' + str(IpPerms['ToPort']))
                    # print(IpPerms)
                    for IpRanges in IpPerms['IpRanges']:
                        if (IpRanges['CidrIp'] == '0.0.0.0/0'):
                            weak_sgs.append(sg['GroupId'])
    print (list(set(weak_sgs)))
    print('')

