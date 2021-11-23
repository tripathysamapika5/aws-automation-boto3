import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.aws_resources.client_locator import EC2Client
from src.aws_resources.resource_locator import EC2Resource

from src.ec2.ec2 import EC2


def describe_instance():    
    ec2_client_service = EC2Client()
    ec2 = EC2().set_client(ec2_client_service)
    
    all_ec2_response = ec2.describe_ec2_instances()
    print('All EC2 responses : {}'.format(all_ec2_response))

def disable_ec2_instance_api_termination():
    ec2_client_service = EC2Client()
    ec2 = EC2().set_client(ec2_client_service)
    
    instance_id = 'i-04829cb2b342ca34a'
    ec2.disable_ec2_instance_api_termination(instance_id, True)
    print("Disabled the api termination for ec2 instance {}".format(instance_id))

def enable_ec2_instance_api_termination():
    ec2_client_service = EC2Client()
    ec2 = EC2().set_client(ec2_client_service)
    
    instance_id = 'i-04829cb2b342ca34a'
    ec2.disable_ec2_instance_api_termination(instance_id, False)
    print("Enabled the api termination for ec2 instance {}".format(instance_id))

    
def stop_instances_with_client():
    
    ec2_client_service = EC2Client()
    ec2 = EC2().set_client(ec2_client_service)

    instance_ids = [instance.instance_id for instance in ec2.get_all_ec2_instances()]    
    stopped_ec2_insatnce_response = ec2.stop_ec2_instances(instance_ids)
    print("Stopped instances response : {}...".format(stopped_ec2_insatnce_response))

def stop_instances_with_resource():
    
    ec2_rescource_service = EC2Resource()
    ec2 = EC2().set_resource(ec2_rescource_service)

    instance_ids = [instance.instance_id for instance in ec2.get_all_ec2_instances()]    
    stopped_ec2_insatnce_response = ec2.stop_ec2_instances(instance_ids)
    print("Stopped instances response : {}...".format(stopped_ec2_insatnce_response))


def start_instances_with_client():
    ec2_client_service = EC2Client()
    ec2 = EC2().set_client(ec2_client_service)

    instance_ids = [instance.instance_id for instance in ec2.get_all_ec2_instances()]   
    starteted_ec2_insatnce_response = ec2.start_ec2_instances(instance_ids)
    print("Started instances response : {}...".format(starteted_ec2_insatnce_response))

def start_instances_with_resource():
    ec2_rescource_service = EC2Resource()
    ec2 = EC2().set_resource(ec2_rescource_service)

    instance_ids = [instance.instance_id for instance in ec2.get_all_ec2_instances()]   
    starteted_ec2_insatnce_response = ec2.start_ec2_instances(instance_ids)
    print("Started instances response : {}...".format(starteted_ec2_insatnce_response))



def terminate_instances_with_client():
    ec2_client_service = EC2Client()
    ec2 = EC2().set_client(ec2_client_service)

    instance_ids = [instance.instance_id for instance in ec2.get_all_ec2_instances()]   
    terminated_ec2_insatnce_response = ec2.terminate_ec2_instances(instance_ids)
    print("Terminated instances response : {}...".format(terminated_ec2_insatnce_response))

def terminate_instances_with_resoure():
    ec2_rescource_service = EC2Resource()
    ec2 = EC2().set_resource(ec2_rescource_service)

    instance_ids = [instance.instance_id for instance in ec2.get_all_ec2_instances()]   
    terminated_ec2_insatnce_response = ec2.terminate_ec2_instances(instance_ids)
    print("Terminated instances response : {}...".format(terminated_ec2_insatnce_response))



def print_all_ec2_instances():
    ec2_client_service = EC2Client()
    ec2_2 = EC2().set_client(ec2_client_service)
           
    print("printing using client...")        
    for instance in ec2_2.get_all_ec2_instances():
        print(instance)
        

    ec2_rescource_service = EC2Resource()
    ec2_1 = EC2().set_resource(ec2_rescource_service)
    
    print("printing using resource...")
    for instance in ec2_1.get_all_ec2_instances():
        print(instance)
        


    ec2_resource_service = EC2Resource(region_name="us-west-1") 
    ec2_1 = EC2().set_resource(ec2_resource_service)

    
    print("printing using resource...")
    for instance in ec2_1.get_all_ec2_instances():
        print(instance)

    ec2_client_service = EC2Client(region_name="us-west-1")
    ec2_2 = EC2().set_client(ec2_client_service)
           
    print("printing using client...")        
    for instance in ec2_2.get_all_ec2_instances():
        print(instance)
        
def print_region_available_for_ec2_service():
    

    ec2_client_service = EC2Client()
    ec2_2 = EC2().set_client(ec2_client_service)
           
    print("printing using client...")        
    for region in ec2_2.get_region_available_for_ec2_service():
        print(region)

    ec2_rescource_service = EC2Resource()
    ec2_1 = EC2().set_resource(ec2_rescource_service)
    
    print("printing using resource...")
    for region in ec2_2.get_region_available_for_ec2_service():
        print(region)
        
        
if __name__ == '__main__':
    pass
    # describe_instance()
    # disable_ec2_instance_api_termination()
    # stop_instances_with_client()
    # start_instances_with_client()
    # stop_instances_with_resource()
    # start_instances_with_resource()
    # terminate_instances() # it will fail as api_termination is disabled
    # enable_ec2_instance_api_termination()
    # terminate_instances_with_client()
    # terminate_instances_with_resoure()
    print_all_ec2_instances()
    # print_region_available_for_ec2_service()
    