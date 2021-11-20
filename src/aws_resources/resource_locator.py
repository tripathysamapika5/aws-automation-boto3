import boto3

class ResourceLocator:
    def __init__(self, service_name, profile_name, region_name): 
        self._resource = boto3.session.Session(profile_name=profile_name, region_name = region_name).resource(service_name)
    def get_instance(self): 
        return self._resource
    
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