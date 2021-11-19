import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.aws_resources.client_locator import EC2Client
from src.aws_resources.resource_locator import EC2Resource

from src.ec2.ec2 import EC2


def describe_instance():    
    ec2_client = EC2Client().get_client()
    ec2 = EC2().set_client(ec2_client)
    
    all_ec2_response = ec2.describe_ec2_instances()
    print('All EC2 responses : {}'.format(all_ec2_response))

def disable_ec2_instance_api_termination():
    ec2_client = EC2Client().get_client()
    ec2 = EC2().set_client(ec2_client)
    
    instance_id = 'i-04829cb2b342ca34a'
    ec2.disable_ec2_instance_api_termination(instance_id, True)
    print("Disabled the api termination for ec2 instance {}".format(instance_id))

def enable_ec2_instance_api_termination():
    ec2_client = EC2Client().get_client()
    ec2 = EC2().set_client(ec2_client)
    
    instance_id = 'i-04829cb2b342ca34a'
    ec2.disable_ec2_instance_api_termination(instance_id, False)
    print("Enabled the api termination for ec2 instance {}".format(instance_id))

    
def stop_instances():
    ec2_client = EC2Client().get_client()
    ec2 = EC2().set_client(ec2_client)

    instance_ids = ['i-059e2eca0b6118fd0', 'i-04829cb2b342ca34a']    
    stopped_ec2_insatnce_response = ec2.stop_ec2_instances(*instance_ids)
    print("Stopped instances : {}...".format(','.join(instance_ids)))


def start_instances():
    ec2_client = EC2Client().get_client()
    ec2 = EC2().set_client(ec2_client)

    instance_ids = ['i-059e2eca0b6118fd0', 'i-04829cb2b342ca34a']    
    starteted_ec2_insatnce_response = ec2.start_ec2_instances(*instance_ids)
    print("Started instances : {}...".format(','.join(instance_ids)))

def terminate_instances():
    ec2_client = EC2Client().get_client()
    ec2 = EC2().set_client(ec2_client)

    instance_ids = ['i-059e2eca0b6118fd0', 'i-04829cb2b342ca34a']    
    terminated_ec2_insatnce_response = ec2.terminate_ec2_instances(*instance_ids)
    print("Terminated instances : {}...".format(','.join(instance_ids)))


def print_all_ec2_instances():
    ec2_client = EC2Client().get_client()
    ec2_2 = EC2().set_client(ec2_client)
           
    print("printing using client...")        
    for instance in ec2_2.get_all_ec2_instances():
        print(instance)

    ec2_rescource = EC2Resource().get_instance()    
    ec2_1 = EC2().set_resource(ec2_rescource)
    
    print("printing using resource...")
    for instance in ec2_1.get_all_ec2_instances():
        print(instance)
        

    ec2_rescource = EC2Resource(region_name="us-west-1").get_instance()    
    ec2_1 = EC2().set_resource(ec2_rescource)
    
    print("printing using resource...")
    for instance in ec2_1.get_all_ec2_instances():
        print(instance)

    ec2_client = EC2Client(region_name="us-west-1").get_client()
    ec2_2 = EC2().set_client(ec2_client)
           
    print("printing using client...")        
    for instance in ec2_2.get_all_ec2_instances():
        print(instance)

if __name__ == '__main__':
    print("Testing ec2 deployments")
    # describe_instance()
    # disable_ec2_instance_api_termination()
    # stop_instances()
    # start_instances()
    # terminate_instances() # it will fail as api_termination is disabled
    # enable_ec2_instance_api_termination()
    # terminate_instances()
    print_all_ec2_instances()
    