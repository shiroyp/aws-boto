#!/usr/bin/env python
from boto.dynamodb2 import connect_to_region
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item

my_table_name='landsat'
my_aws_region='eu-west-1'


conn = connect_to_region(my_aws_region)
table = Table(my_table_name, connection=conn)


#Fetching the table status
tab_describe = table.describe()
tab_details = tab_describe['Table']

print tab_details['TableName']
print tab_details['TableArn']
print tab_details['TableStatus']


# Here, my hash key is entityId and range key is acquisitionDate
results = table.query_2(
    entityId__eq='LC80500162015170LGN00',
    acquisitionDate__beginswith='2015')

#Iterating through the results
for each in results:
    #Fetching the keys in each item and reading the values
    # for key in Item.keys(each):
    #     print key + ":" + each[key]
    # print " "

    data=Item.get_keys(each)
    print data
