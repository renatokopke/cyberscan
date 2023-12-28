import logging
from datetime import datetime

import boto3 as boto3
from botocore.exceptions import ClientError
from decouple import config
from pytz import timezone

from core.settings import BASE_DIR


class Tools:
    def __init__(self):
        pass

    def logodata(self):

        f = open(str(BASE_DIR)+'/core/cyberscan.dat')

        data = f.read()

        f.close()

        return data


class ToolsS3:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config('AWS_UPLOAD_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_UPLOAD_SECRET_KEY'),
        )

        self.session = boto3.Session(
            aws_access_key_id=config('AWS_UPLOAD_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_UPLOAD_SECRET_KEY'),
        )

    def create_presigned_url(self, bucket_name, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        # Generate a presigned URL for the S3 object
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': str(object_name)
                },
                ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        s3 = self.session.resource('s3')

        if object_name is None:
            object_name = file_name

        # # Upload the file
        try:
            s3.meta.client.upload_file(
                Filename=file_name,
                Bucket=bucket,
                Key=object_name
            )
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def delete_bucket(self, bucketname, keyprefix):
        '''
        Recusively delete all keys with given prefix from the named bucket
        Stolen from http://stackoverflow.com/a/10055320/141084
        '''
        s3 = boto3.connect_s3(
            aws_access_key_id=config('AWS_UPLOAD_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_UPLOAD_SECRET_KEY'))

        bucket = s3.get_bucket(bucketname, validate=False)
        bucketListResultSet = bucket.list(prefix=keyprefix)
        return bucket.delete_keys([key.name for key in bucketListResultSet])

    # connect to s3 and delete the file
    def delete_s3_file(self, file_path, bucket):
        print(f"Deleting {file_path}")
        self.s3_client.delete_object(Bucket=bucket, Key=file_path)

        return True