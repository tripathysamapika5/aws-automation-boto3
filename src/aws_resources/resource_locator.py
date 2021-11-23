import boto3

from src.aws_resources.waiter import ClientWaiterService

class ResourceLocator:
    def __init__(self, service_name, profile_name, region_name): 
        self.__resource = boto3.session.Session(profile_name=profile_name, region_name = region_name).resource(service_name)
        self.__client = self.__resource.meta.client
        self.__waiter_service = ClientWaiterService(self.__client)
        
    def get_resource(self): 
        return self.__resource
    def get_client(self):
        return self.__client
    def get_client_waiter_from_resource_object(self):
        return self.__waiter_service
        
    
class EC2Resource(ResourceLocator):
    """It will return EC2 resource

    Args:
        ResourceLocator (String)
    """
    def __init__(self, profile_name = "samapika", region_name = "us-east-1"): 
        super().__init__('ec2', profile_name, region_name)
    
class IamResource(ResourceLocator):
    """It will return IAM resource

    Args:
        ResourceLocator (String)
    """
    def __init__(self, profile_name = "samapika", region_name = "us-east-1"): 
        super().__init__('iam', profile_name, region_name)
        
class S3Resource(ResourceLocator):
    """It will return S3 resource

    Args:
        ResourceLocator (String)
    """
    def __init__(self, profile_name = "samapika", region_name = "us-east-1"): 
        super().__init__('s3', profile_name, region_name)