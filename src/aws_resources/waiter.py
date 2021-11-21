class ClientWaiterService:
    
    def __init__(self, client):
        self.__client = client
        
    def wait_till_instance_status_running(self, instance_ids_list):
        self.__client.get_waiter('instance_running').wait(InstanceIds = instance_ids_list)
    
    def wait_till_instance_status_stopped(self, instance_ids_list):
        self.__client.get_waiter('instance_stopped').wait(InstanceIds = instance_ids_list)
    
    def wait_till_instance_status_terminated(self, instance_ids_list):
        self.__client.get_waiter('instance_terminated').wait(InstanceIds = instance_ids_list)
        
    def wait_till_instance_exists(self, instance_ids_list):
        self.__client.get_waiter('instance_exists').wait(InstanceIds = instance_ids_list)
    
    def wait_till_key_pair_exists(self, key_names):
        self.__client.get_waiter('key_pair_exists').wait(KeyNames = key_names)
        
    def wait_till_security_group_exists(self, group_ids):
        self.__client.get_waiter('security_group_exists').wait(GroupIds = group_ids, WaiterConfig = {'MaxAttempts' : 20})
        
    def wait_till_vpc_available(self, vpc_ids):
        self.__client.get_waiter('vpc_available').wait(VpcIds = vpc_ids) 
        
    def wait_till_subnet_available(self, subnet_ids):
        self.__client.get_waiter('subnet_available').wait(SubnetIds = subnet_ids) 
        
    
    
    