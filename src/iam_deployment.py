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

def create_user_with_console_access_client():
    iam_client_service = IamClient()
    iam = IAMService().set_client(iam_client_service)
    iam.create_user(user_name= "admin_console", policy_arn="arn:aws:iam::aws:policy/AdministratorAccess", console_access=True, programmatic_access=False)

def create_user_with_programmatic_access_client():
    iam_client_service = IamClient()
    iam = IAMService().set_client(iam_client_service)
    iam.create_user(user_name= "admin_program", policy_arn="arn:aws:iam::aws:policy/AdministratorAccess", console_access=False, programmatic_access=True)

def create_user_with_console_and_programmatic_access_client():
    iam_client_service = IamClient()
    iam = IAMService().set_client(iam_client_service)
    iam.create_user(user_name= "admin_program_console", policy_arn="arn:aws:iam::aws:policy/AdministratorAccess")


def create_user_with_console_access_resource():
    iam_resource_service = IamResource()
    iam = IAMService().set_resource(iam_resource_service)
    iam.create_user(user_name= "admin_console", policy_arn="arn:aws:iam::aws:policy/AdministratorAccess", console_access=True, programmatic_access=False)

def create_user_with_programmatic_access_resource():
    iam_resource_service = IamResource()
    iam = IAMService().set_resource(iam_resource_service)
    iam.create_user(user_name= "admin_program", policy_arn="arn:aws:iam::aws:policy/AdministratorAccess", console_access=False, programmatic_access=True)

def create_user_with_console_and_programmatic_access_resource():
    iam_resource_service = IamResource()
    iam = IAMService().set_resource(iam_resource_service)
    iam.create_user(user_name= "admin_program_console", policy_arn="arn:aws:iam::aws:policy/AdministratorAccess")


if __name__ == '__main__':
    # print_all_users();
    # print_users()
    # print_all_groups()
    # print_groups()
    # create_user_with_console_access_client()
    # create_user_with_programmatic_access_client()
    # create_user_with_console_and_programmatic_access_client()
    create_user_with_console_access_resource()
    create_user_with_programmatic_access_resource()
    create_user_with_console_and_programmatic_access_resource()

    pass