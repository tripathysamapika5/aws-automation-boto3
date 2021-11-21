import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.aws_resources.resource_locator import IamResource
from src.aws_resources.client_locator import IamClient
from src.iam.iam import IAM


def print_all_users():
    iam_resource_service = IamResource()
    iam_client_service = IamClient()
    
    iam1 = IAM().set_resource(iam_resource_service)
    
    print("printing using resource...")
    for user in iam1.get_all_users():
        print(user)
        
    iam2 = IAM().set_client(iam_client_service) 
       
    print("printing using client...")        
    for user in iam2.get_all_users():
        print(user)


if __name__ == '__main__':
    print_all_users();
    pass