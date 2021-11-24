import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.aws_resources.resource_locator import IamResource
from src.aws_resources.client_locator import IamClient
from src.iam.iam import IAMService


def print_all_users():
    iam_resource_service = IamResource()
    iam_client_service = IamClient()
    
    iam1 = IAMService().set_resource(iam_resource_service)
    
    print("printing using resource...")
    for user in iam1.get_users():
        print(user)
        
    iam2 = IAMService().set_client(iam_client_service) 
       
    print("printing using client...")        
    for user in iam2.get_users():
        print(user)

def print_users():
    iam_resource_service = IamResource()
    iam_client_service = IamClient()
    
    iam1 = IAMService().set_resource(iam_resource_service)
    
    print("printing using resource...")
    for user in iam1.get_users(["s3_developer", "ec2_developer"]):
        print(user)
        
    iam2 = IAMService().set_client(iam_client_service) 
       
    print("printing using client...")        
    for user in iam2.get_users(["s3_developer", "ec2_developer"]):
        print(user)

def print_all_groups():
    iam_resource_service = IamResource()
    iam_client_service = IamClient()

    iam1 = IAMService().set_resource(iam_resource_service)

    print("printing using resource...")
    for group in iam1.get_groups():
        print(group)

    iam2 = IAMService().set_client(iam_client_service)

    print("printing using client...")
    for group in iam2.get_groups():
        print(group)

def print_groups():
    iam_resource_service = IamResource()
    iam_client_service = IamClient()

    iam1 = IAMService().set_resource(iam_resource_service)

    print("printing using resource...")
    for group in iam1.get_groups(["developers"]):
        print(group)

    iam2 = IAMService().set_client(iam_client_service)

    print("printing using client...")
    for group in iam2.get_groups(["developers"]):
        print(group)

if __name__ == '__main__':
    # print_all_users();
    print_users()
    # print_all_groups()
    print_groups()
    pass