# import boto3

# # Get the service resource.
# dynamodb = boto3.resource('dynamodb')

# # Instantiate a table resource object without actually
# # creating a DynamoDB table. Note that the attributes of this table
# # are lazy-loaded: a request is not made nor are the attribute
# # values populated until the attributes
# # on the table resource are accessed or its load() method is called.
# table = dynamodb.Table('users')

# # Print out some data about the table.
# # This will cause a request to be made to DynamoDB and its attribute
# # values will be set based on the response.
# print(table.creation_date_time)


dict = ['lukasavic', [{'Name': 'sub', 'Value': '23ed879c-257b-4121-bef5-db0b48458d81'}, {'Name': 'email_verified', 'Value': 'true'}, {'Name': 'email', 'Value': 'lukasavic18@gmail.com'}], {'RequestId': '135a4267-070f-4ba5-878a-e60f53661496', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Wed, 13 Oct 2021 18:06:52 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '195', 'connection': 'keep-alive', 'x-amzn-requestid': '135a4267-070f-4ba5-878a-e60f53661496'}, 'RetryAttempts': 0}]
dict1 = {'ResponseMetadata': {'RequestId': '1OGJGKS6072BVS2SJS5JQONA3BVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Wed, 13 Oct 2021 19:44:33 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'connection': 'keep-alive', 'x-amzn-requestid': '1OGJGKS6072BVS2SJS5JQONA3BVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
respondee = {'city': None, 'phone_number': None, 'employer': None, 'email': 'nekitamomail@gmail.com', 'name': None, 'birthday': None, 'jobtitle': None, 'age': None}

lista = list(respondee.values())
city = lista[0]
phone_number = lista[1]
employer = lista[2]
name = lista[4]
birthday = lista[5]
jobtitle = lista[6]
age = lista[7]
