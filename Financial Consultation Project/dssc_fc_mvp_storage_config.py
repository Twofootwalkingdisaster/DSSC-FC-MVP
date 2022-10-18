# This class is used to store the AWS S3 access keys
# Use this key to extract the necessary stock data from the AWS S3 storage

class StorageConfig:

    # These keys will be prone to change if any options that alter the properties of the database are changed
    # Hence this can lead to a potential security error
    # Tip: Please update the access keys whenever the properties of the database are changed

    # The below constant stores the access key ID
    AWS_ACCESS_KEY_ID = 'AKIASO7H4JOY4M5UADGU'

    # The below constant stores the secret access key
    AWS_SECRET_ACCESS_KEY = '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'

    # File path main folder
    AWS_BUCKET_NAME = 'dssc-fc-mvp'

    # File path sub folder 1, the hierarchy follows with a number in increasing order
    AWS_BUCKET_SUB_FOLDER_1 = 'data-collection'
