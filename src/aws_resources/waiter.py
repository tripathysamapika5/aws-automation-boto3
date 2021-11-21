class ClientWaiterService:
    
    def __init__(self, client):
        self.__client = client
        
    def wait_till_instance_status_running(self, instance_ids_list):
        """It will wait for the instances to come to the status running

        Args:
            instance_ids_list (list(str))
        """
        self.__client.get_waiter('instance_running').wait(InstanceIds = instance_ids_list)
    
    def wait_till_instance_status_stopped(self, instance_ids_list):
        """It will wait for the instances to come to the status stopped

        Args:
            instance_ids_list (list(str))
        """
        self.__client.get_waiter('instance_stopped').wait(InstanceIds = instance_ids_list)
    
    def wait_till_instance_status_terminated(self, instance_ids_list):
        """It will wait for the instances to come to the status terminated

        Args:
            instance_ids_list (list(str))
        """
        self.__client.get_waiter('instance_terminated').wait(InstanceIds = instance_ids_list)
        
    def wait_till_instance_exists(self, instance_ids_list):
        """It will wait for the instances to get launched

        Args:
            instance_ids_list (list(str))
        """
        self.__client.get_waiter('instance_exists').wait(InstanceIds = instance_ids_list)
    
    def wait_till_key_pair_exists(self, key_names):
        """It will wait for the keypair to be created

        Args:
            key_names (list(key pair name))
        """
        self.__client.get_waiter('key_pair_exists').wait(KeyNames = key_names)
        
    def wait_till_security_group_exists(self, group_ids):
        """It will wait for the security group to be created

        Args:
            key_names (list(security group id))
        """
        self.__client.get_waiter('security_group_exists').wait(GroupIds = group_ids, WaiterConfig = {'MaxAttempts' : 20})
        
    def wait_till_vpc_available(self, vpc_ids):
        """It will wait for the vpcs to be created

        Args:
            key_names (list(vpc id))
        """
        self.__client.get_waiter('vpc_available').wait(VpcIds = vpc_ids) 
        
    def wait_till_subnet_available(self, subnet_ids):
        """It will wait for the subnets to be created

        Args:
            key_names (list(subnet id))
        """
        self.__client.get_waiter('subnet_available').wait(SubnetIds = subnet_ids) 
        
    
    
    