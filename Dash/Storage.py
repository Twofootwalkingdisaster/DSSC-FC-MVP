import boto3
import json
import pandas as pd
from io import BytesIO


# Created the function which connects the code with AWS S3 and
# take the input as company name and gives us the data of that comapny
# which we have already stored in S3 bucket
with open('DSSC-FC-MVP-Configuration.json', 'r') as openfile:
    json_object = json.load(openfile)


class GetFile:
    def get_file(company_name):
        client = boto3.client('s3',
                              aws_access_key_id=json_object['aws_access_key_id'],
                              aws_secret_access_key=json_object['aws_secret_access_key'])
        file = client.get_object(Bucket='dssc-fc-mvp',
                                 Key='data-collection/' + company_name + '_data.csv')
        read_file = file['Body'].read()
        read_file_csv = pd.read_csv(BytesIO(read_file))

        return read_file_csv
