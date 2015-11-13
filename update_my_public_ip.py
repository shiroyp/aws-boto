#!/usr/bin/env python3
# I use this script to update my security group sg-9df995f8 with my current public IP. 
# It removes all the existing SSH and RDP access rules from the security group.

__author__ = 'Shiroy'

from boto3.session import Session
from urllib.request import urlopen
from re import findall


# Find out my home public IP
# url = "http://checkip.dyndns.org"
url = "http://www.whatismypublicip.com/"
request = urlopen(url)
data = request.read()
ip_data = findall(b"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", data)
# regex to extract ip from the response data
# ip_data = findall(b'[0-9]+(?:\.[0-9]+){3}', data)
# ip_data = findall(b'[\d.-]+', data)
ip = str(ip_data[0]).split("'")[1]
my_ip=ip+'/'+'32'
print('Current Public IP : ' + my_ip)

session = Session()
ec2=session.resource('ec2',region_name='eu-west-1')
# ec2 = boto3.resource('ec2')
security_group = ec2.SecurityGroup('sg-9df995f8')
print('Security Group Name :' + security_group.group_name)
for current_rules in security_group.ip_permissions:
    print(current_rules)


for ingress in security_group.ip_permissions:


    if ingress['IpProtocol'] == 'tcp' and ingress['FromPort'] <= 22 and ingress['ToPort'] >= 22:
        for ipranges in ingress['IpRanges']:
            if ipranges['CidrIp'] != my_ip:
                print('Removing ingress SSH for unwanted/old IP....' + ipranges['CidrIp'])
                try:
                    print(security_group.revoke_ingress(
                        IpProtocol=ingress['IpProtocol'],
                        FromPort=ingress['ToPort'],
                        ToPort=ingress['ToPort'],
                        CidrIp=ipranges['CidrIp']
                    ))
                except Exception as e:
                    print(e)

    if ingress['IpProtocol'] == 'tcp' and ingress['ToPort'] <= 3389 and ingress['ToPort'] >= 3389:
        for ipranges in ingress['IpRanges']:
            if ipranges['CidrIp'] != my_ip:
                print('Removing ingress RDP for unwanted/old IP....' + ipranges['CidrIp'])
                try:
                    print(security_group.revoke_ingress(
                        IpProtocol=ingress['IpProtocol'],
                        FromPort=ingress['ToPort'],
                        ToPort=ingress['ToPort'],
                        CidrIp=ipranges['CidrIp']
                    ))
                except Exception as e:
                    print(e)


print('Adding ingress rule to allow SSH connections from Home IP....' + my_ip)
try:
    print(security_group.authorize_ingress(
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        CidrIp=my_ip
    ))
except Exception as e:
    print(e)

print('Adding ingress rule to allow RDP connections from Home IP....' + my_ip)
try:
    print(security_group.authorize_ingress(
        IpProtocol='tcp',
        FromPort=3389,
        ToPort=3389,
        CidrIp=my_ip
    ))
except Exception as e:
    print(e)

print('The current set of rules is as follows.....')
for new_rules in security_group.ip_permissions:
    print(new_rules)
