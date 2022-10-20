# This Python file is the main file and will be used to download the publicly \
# available stock data
# To download the stock data we use Yfinance (Yahoo Finance) library
# The storage we have used in this Amazon Web Services S3 \
# it's a simple cloud storage that provides object storage through a web service interface

import datetime
from datetime import date
from io import BytesIO
import yfinance as yfin
import boto3
import pandas as pd
import os
import json

# Maintain a global instance of the configuration file
storage_config = None

# Maintain a global instance of the client variable
s3_client = None


class ConnectToS3DataBase:
    # Here this method will initiate the connection request to the S3 database
    @staticmethod
    def client_connection_authentication():
        # Client connection authentication
        global s3_client
        # This Null check is done to prevent any crash issue that is caused by null values
        if s3_client is None:
            s3_client = boto3.client('s3',
                                     aws_access_key_id=storage_config['aws_access_key_id'],
                                     aws_secret_access_key=storage_config['aws_secret_access_key'])

            print(f'Client authentication has been created {s3_client}')


# This class is responsible to fetch the .csv data files from S3 Database
class S3DatabaseActions:
    # This method below will browse through the directory in the local system and \
    # update the S3 database
    @staticmethod
    def update_s3_database():
        for file in os.listdir():
            upload_file_bucket = storage_config['aws_bucket_name']
            upload_file_key = storage_config['aws_bucket_sub_folder_1']
            s3_client.upload_file(file,
                                  upload_file_bucket,
                                  upload_file_key)

    # This method below will get the csv file for a specific company from S3 database
    @staticmethod
    def fetch_file_from_s3_database(company):
        file = s3_client.get_object(Bucket=storage_config['aws_bucket_name'],
                                    Key=storage_config['aws_bucket_sub_folder_1']+'/'+company+'_data.csv')
        read_file = file['Body'].read()
        read_file_csv = pd.read_csv(BytesIO(read_file))

        # return the read file
        return read_file_csv

    # This function will pull the data for a particular ticker symbol


class YfinanceDataRequest:
    # Given this method below is executed
    # When we need the latest stock data
    # Then the latest stock information is pulled in .csv format using the yfinance library
    @staticmethod
    def pull_latest_stock_data(company_name):
        current_date = datetime.datetime.now()
        stock_data = yfin.download(company_name,
                                   start="2020-11-01",
                                   end=current_date,
                                   interval='1h')

        stock_data['DateTime'] = stock_data.index
        stock_data.set_index('DateTime',
                             inplace=True)

        return stock_data


# This class here initializes all the services for the start of the project
class InitializeDSSCService:
    # The static method below initializes all services
    @staticmethod
    def initialize_dssc_service():

        # Load the created configuration file
        configuration_file = open('dssc_fc_mvp_configuration.json', 'r')
        global storage_config
        storage_config = json.load(configuration_file)
        print(storage_config)

        # Run the client authentication method
        ConnectToS3DataBase.client_connection_authentication()
