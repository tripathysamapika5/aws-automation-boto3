import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.aws_resources.resource_locator import S3Resource
from src.aws_resources.client_locator import S3Client

from src.s3.s3 import S3


def print_all_buckets():
    s3_resource_service = S3Resource(profile_name = "s3_developer")
    s3 = S3().set_resource(s3_resource_service)
    
    print("Printing all buckets using AWS resource object...")
    for bucket in s3.get_all_buckets():
        print(bucket)

    s3_client_service = S3Client(profile_name = "s3_developer")
    s3_new = S3().set_client(s3_client_service)
    
    print("Printing all buckets using AWS client object...")
    for bucket in s3_new.get_all_buckets():
        print(bucket)


if __name__ == '__main__':
    print_all_buckets();