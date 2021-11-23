import sys
import os
import boto3


PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from  src.aws_resources.waiter import ClientWaiterService


class ClientLocator:
    def __init__(self, service_name, profile_name, region_name ): 
        self.__client = boto3.session.Session(profile_name = profile_name, region_name = region_name).client(service_name)
        self.__waiter_service = ClientWaiterService(self.__client)
    def get_client(self): 
        return self.__client
    def get_waiter(self):
        return self.__waiter_service 
 
class EC2Client(ClientLocator):
    """It will return EC2 client

    Args:
        ClientLocator (String)
    """
    def __init__(self, profile_name = "samapika", region_name = "us-east-1"): 
        super().__init__('ec2', profile_name, region_name)
        
class IamClient(ClientLocator):
    """It will return IAM client

    Args:
        ClientLocator (String)
    """

    def __init__(self, profile_name = "samapika",region_name = "us-east-1"): 
        super().__init__('iam', profile_name, region_name)
        
class S3Client(ClientLocator):
    """It will return S3 client

    Args:
        ClientLocator (String)
    """
    def __init__(self, profile_name = "samapika",region_name = "us-east-1"): 
        super().__init__('s3', profile_name, region_name)
        
class STSClient(ClientLocator):
    """It will return STS client

    Args:
        ClientLocator (String)
    """
    def __init__(self, profile_name = "samapika",region_name = "us-east-1"): 
        super().__init__('sts', profile_name, region_name)