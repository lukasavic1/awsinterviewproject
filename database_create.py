import boto3

dynamodb = boto3.resource('dynamodb',
                    region_name='eu-central-1',
                    aws_access_key_id='AKIARG535AD7AZAREKBU',
                    aws_secret_access_key='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')
table_name = 'testing'

def create_dynamodb():
    table = dynamodb.Table(table_name)
    print(table.item_count) 
    return table
    # existing_tables = dynamodb.list_tables()['TableNames']

    # if table_name not in existing_tables:
    #     table = dynamodb.create_table(
    #         TableName='testdatabase',
    #         GlobalSecondaryIndexes= 
    #         [ 
    #             { 
    #                 IndexName = 'kurac',
    #                 KeySchema = [ 
    #                     { 
    #                     AttributeName= "string",
    #                     KeyType= "string"
    #                     }
    #                 ],
    #                 Projection= { 
    #                     NonKeyAttributes= [ "string" ],
    #                     ProjectionType= "string"
    #                 },
    #                 ProvisionedThroughput { 
    #                     ReadCapacityUnits=number,
    #                     WriteCapacityUnits= number
    #                 }
    #             }
    #         ],
    #         KeySchema=[
    #             {
    #                 'AttributeName': 'email',
    #                 'KeyType': 'HASH'
    #             },
    #             {
    #                 'AttributeName': 'name',
    #                 'KeyType': 'RANGE'
    #             },
    #             {
    #                 'AttributeName': 'age',
    #                 'KeyType': 'RANGE'
    #             },
    #             {
    #                 'AttributeName': 'birthday',
    #                 'KeyType': 'RANGE'
    #             },
    #             {
    #                 'AttributeName': 'jobtitle',
    #                 'KeyType': 'RANGE'
    #             },
    #             {
    #                 'AttributeName': 'employer',
    #                 'KeyType': 'RANGE'
    #             },
    #             {
    #                 'AttributeName': 'city',
    #                 'KeyType': 'RANGE'
    #             },
    #             {
    #                 'AttributeName': 'phone_number',
    #                 'KeyType': 'RANGE'
    #             }
    #         ],
    #         AttributeDefinitions=[
    #             {
    #                 'AttributeName': 'email',
    #                 'AttributeType': 'S'
    #             },
    #             {
    #                 'AttributeName': 'name',
    #                 'AttributeType': 'S'
    #             },
    #             {
    #                 'AttributeName': 'age',
    #                 'AttributeType': 'N'
    #             },
    #             {
    #                 'AttributeName': 'birthday',
    #                 'AttributeType': 'S'
    #             },
    #             {
    #                 'AttributeName': 'jobtitle',
    #                 'AttributeType': 'S'
    #             },
    #             {
    #                 'AttributeName': 'employer',
    #                 'AttributeType': 'S'
    #             },
    #             {
    #                 'AttributeName': 'city',
    #                 'AttributeType': 'S'
    #             },
    #             {
    #                 'AttributeName': 'phone_number',
    #                 'AttributeType': 'N'
    #             }
    #         ],
    #         ProvisionedThroughput={
    #             'ReadCapacityUnits': 1,
    #             'WriteCapacityUnits': 1
    #         }
    #     )

    #     # Wait until the table exists.
    #     table.meta.client.get_waiter('table_exists').wait(TableName='testdatabase')
    # else:
    # # Print out some data about the table.
    # print(table.item_count)