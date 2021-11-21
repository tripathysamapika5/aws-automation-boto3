import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.aws_resources.client_locator import EC2Client
from src.aws_resources.resource_locator import EC2Resource

from src.ec2.volume import VolumeService

def print_all_volumes():
    ec2_client_service = EC2Client()
    volume_2 = VolumeService().set_client(ec2_client_service)
           
    print("printing using client...")        
    for volume in volume_2.get_all_volumes():
        print(volume)

    ec2_rescource_service = EC2Resource()
    volume_1 = VolumeService().set_resource(ec2_rescource_service)
    
    print("printing using resource...")
    for volume in volume_1.get_all_volumes():
        print(volume)
        
if __name__ == '__main__':
    print("Testing volume deployments")
    # describe_instance()
    # disable_ec2_instance_api_termination()
    # stop_instances()
    # start_instances()
    # terminate_instances() # it will fail as api_termination is disabled
    # enable_ec2_instance_api_termination()
    # terminate_instances()
    print_all_volumes()