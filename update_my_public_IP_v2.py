#!/usr/bin/env python3
# I use this script to update my security group sg-9df995f8 with my current public IP. 
# It removes all the access rules from the security group which are not matching with Public IP.

__author__ = 'Shiroy'

from boto3.session import Session
from urllib.request import urlopen
from re import findall

my_region='eu-west-1'
my_security_group='sg-9df995f8'
allowed_ports=(22,3389,8020,50010,50075,50475,50020,50070,50470,50090,8040,8042,8032,8033,8031,8030,8088,10000,18080)


url = "http://www.whatismypublicip.com/"
request = urlopen(url)
data = request.read()
ip_data = findall(b"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", data)
ip = str(ip_data[0]).split("'")[1]
my_ip=ip+'/'+'32'
print('Current Public IP : ' + my_ip)

session = Session()
ec2=session.resource('ec2',region_name=my_region)
security_group = ec2.SecurityGroup(my_security_group)
print('Security Group Name :' + security_group.group_name)

for current_rules in security_group.ip_permissions:
    print(current_rules)

for ingress in security_group.ip_permissions:
    for ipranges in ingress['IpRanges']:
        if ipranges['CidrIp'] != my_ip:
            print('Removing ingress rules with unwanted/old IP....' + ipranges['CidrIp'])
            try:
                security_group.revoke_ingress(
                    IpProtocol=ingress['IpProtocol'],
                    FromPort=ingress['ToPort'],
                    ToPort=ingress['ToPort'],
                    CidrIp=ipranges['CidrIp']
                )
            except Exception as e:
                print(e)

for port in allowed_ports:
    print('Adding ingress rule to allow tcp port ' + str(port) +  ' from Home IP....' + my_ip)
    try:
        security_group.authorize_ingress(
            IpProtocol='tcp',
            FromPort=port,
            ToPort=port,
            CidrIp=my_ip
        )
    except Exception as e:
        print(e)

print('The current set of rules is as follows.....')
for new_rules in security_group.ip_permissions:
    print(new_rules)
