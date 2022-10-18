# This Python file is the main file and will be used to download the publicly \
# available stock data
# To download the stock data we use Yfinance (Yahoo Finance) library
# The storage we have used in this Amazon Web Services S3 \
# it's a simple cloud storage that provides object storage through a web service interface

from dssc_fc_mvp_storage_config import StorageConfig as storage_config
import boto3
import pandas as pd
import os
from io import BytesIO
import json


# Maintain a global instance of the client variable
s3_client = None


# This class will be responsible to connect with the AWS S3 database and extract the data
class ConnectToS3DataBase:
    # Here this method will initiate the connection request to the S3 database
    @staticmethod
    def client_connection_authentication():
        # Client connection authentication
        global s3_client
        # This Null check is done to prevent any crash issue that is caused by null values
        if s3_client is None:
            s3_client = boto3.client('s3',
                                     aws_access_key_id=storage_config.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=storage_config.AWS_SECRET_ACCESS_KEY)


# This class is responsible to fetch the .csv data files from S3 Database
class FetchFilesFromS3Database:
    # This method below will browse through the directory in the local system and \
    # update the S3 database
    @staticmethod
    def update_s3_database():
        for file in os.listdir():
            upload_file_bucket = storage_config.AWS_BUCKET_NAME
            upload_file_key = storage_config.AWS_BUCKET_SUB_FOLDER_1
            s3_client.upload_file(file,
                                  upload_file_bucket,
                                  upload_file_key)

    # This method below will get the csv file for a specific company from S3 database
    @staticmethod
    def fetch_file_from_s3_database(company):
        file = s3_client.get_object(Bucket=storage_config.AWS_BUCKET_NAME,
                                    Key=storage_config.AWS_BUCKET_SUB_FOLDER_1+'/'+company+'_data.csv')
        read_file = file['Body'].read()
        read_file_csv = pd.read_csv(BytesIO(read_file))

        # return the read file
        return read_file_csv


ConnectToS3DataBase.client_connection_authentication()
Data = FetchFilesFromS3Database.fetch_file_from_s3_database('Apple')
print(Data)









