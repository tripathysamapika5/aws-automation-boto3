from src.ec2.region import ServiceRegion

class EC2Instance:
    def __init__(self, 
                 instance_id, 
                 launch_time = None, 
                 instance_type = None, 
                 platform = None, 
                 image_id = None, 
                 public_ip_address = None, 
                 public_dns_name = None, 
                 private_ip_address = None, 
                 private_dns_name = None,
                 state = None, 
                 subnet_id = None, 
                 vpc_id = None,
                 architecture = None,
                 instance_life_cycle = None,
                 volume_ids = None
                ):
        self.instance_id = instance_id
        self.launch_time = launch_time
        self.instance_type = instance_type
        self.platform = platform
        self.image_id = image_id
        self.public_ip_address = public_ip_address
        self.public_dns_name = public_dns_name
        self.state = state
        self.subnet_id = subnet_id
        self.vpc_id = vpc_id
        self.private_ip_address = private_ip_address
        self.private_dns_name = private_dns_name
        self.architecture = architecture
        self.instance_life_cycle = instance_life_cycle
        self.volume_ids = volume_ids
        
    def __str__(self):
        return """Details EC2 instance Id : {}
                launch_time = {},
                instance_type = {},
                platform = {},
                image_id = {},
                public_ip_address = {},
                public_dns_name = {},
                private_ip_address = {},
                private_dns_name = {},
                state = {},
                subnet_id = {},
                vpc_id = {},
                architecture = {},
                instance_life_cycle = {},
                volume_ids  = {}
              """.format(
                  self.instance_id,
                  self.launch_time,
                  self.instance_type,
                  self.platform,
                  self.image_id,
                  self.public_ip_address,
                  self.public_dns_name,
                  self.private_ip_address,
                  self.private_dns_name,
                  self.state,
                  self.subnet_id,
                  self.vpc_id,
                  self.architecture,
                  self.instance_life_cycle,
                  self.volume_ids
                  )
        
        



class EC2:
    """this class provides methods to perform actions on EC2 instances
    
    sample code snippet to create EC2 classes:
    
    from src.aws_resources.client_locator import EC2Client
    from src.aws_resources.resource_locator import EC2Resource

    ec2_client = EC2Client().get_client()
    ec2 = EC2().set_client(ec2_client)
    
    ec2_rescource = EC2Resource().get_instance()    
    ec2_1 = EC2().set_resource(ec2_rescource)
    
    
    """
    def set_client(self, client_service):
        """It will set the AWS client for EC2

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = client_service.get_client();
        self.__client_waiter = client_service.get_waiter();
        self.__resource = None;
        return self;
    
    def set_resource(self, resource_service):
        """It will set the AWS resource for EC2

        Args:
            client (AWS resource)

        Returns:
            IAM: returns the object of type 
        """

        self.__client = None;
        self.__client_waiter = None;
        self.__resource = resource_service.get_resource();
        return self;
    
    def create_key_pair(self, key_name):
        print("Creating a keypair with name : {}".format(key_name))
        if self.__client:
            response = self.__client.create_key_pair(
                KeyName = key_name
            )
            self.__client_waiter.wait_till_key_pair_exists([key_name])
            return response
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def create_security_group(self, group_name, description, vpc_id):
        print("Creating security group with name {} for vpc {}...".format(group_name, vpc_id))
        if self.__client:
            response = self.__client.create_security_group(
                GroupName = group_name, 
                Description = description, 
                VpcId = vpc_id
            )
            group_id = response.get("GroupId")
            self.__client_waiter.wait_till_security_group_exists([group_id])
            return response
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def create_ip_permission_list_for_inbound_rule(self, ip_protocol, source_to_destination_ports, cidr_ip_ranges):
        ip_permissions = []
        for from_port, to_port in source_to_destination_ports:
            ip_permission = {}
            ip_permission['IpProtocol'] = ip_protocol
            ip_permission['FromPort'] = from_port
            ip_permission['ToPort'] = to_port
            ip_permission['IpRanges'] = [{'CidrIp': cidr_ip_ranges}]  
            ip_permissions.append(ip_permission)
        return ip_permissions
        
    def add_inbound_rule_to_sg(self, security_group_id, ip_permissions):
        print("Adding inbound rule(s) to security group {}...".format(security_group_id))
        if self.__client:
            return self.__client.authorize_security_group_ingress(
                GroupId = security_group_id,
                IpPermissions = ip_permissions
            )
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")

    def launch_ec2_instance(self, image_id, instance_type, key_name, min_count, max_count, security_group_id, subnet_id, user_data):
        print("Launching ec2 instance(s) within subnet : {}...".format(subnet_id))
        if self.__client:
            response = self.__client.run_instances(
                ImageId = image_id,
                InstanceType = instance_type,
                KeyName = key_name,
                MinCount = min_count,
                MaxCount = max_count,
                SecurityGroupIds = [security_group_id],
                SubnetId = subnet_id,
                UserData = user_data     
            )
            
            instance_ids = [instance.get("InstanceId") for instance in response.get('Instances')]
            self.__client_waiter.wait_till_instance_exists(instance_ids);
            return response
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def describe_ec2_instances(self):
        print("Describing Ec2 instances...")
        if self.__client:
            return self.__client.describe_instances()
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def disable_ec2_instance_api_termination(self, instance_id, disable_api_termination):
        print("Modifying the api termination to {} for ec2 instance {}".format(not(disable_api_termination), instance_id))
        if self.__client:
            return self.__client.modify_instance_attribute(
                InstanceId = instance_id, 
                DisableApiTermination = {'Value': disable_api_termination} 
            )
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
        
    def __start_ec2_instances_with_client(self, instance_ids):
        filters = [{'Name': 'instance-state-name', 'Values' : ["stopped"]}]
        stopped_instance_ids_list = [instance.instance_id for instance in self.get_all_ec2_instances(list(instance_ids), filters)]
        response = self.__client.start_instances(InstanceIds = stopped_instance_ids_list)
        self.__client_waiter.wait_till_instance_status_running(stopped_instance_ids_list)
        return response
    
    
    def __start_ec2_instances_with_resource(self, instance_ids):
        
        filters = [{'Name': 'instance-state-name', 'Values' : ["stopped"]}]
        stopped_instance_ids_list = [instance.instance_id for instance in self.get_all_ec2_instances(list(instance_ids), filters)]
        
        stopped_instances = list(self.__resource.instances.filter(InstanceIds = stopped_instance_ids_list))
        
        response = self.__resource.instances.filter(InstanceIds = stopped_instance_ids_list).start()
        
        for instance in stopped_instances:
            instance.wait_until_running()
            
        return response
    
    
    def __stop_ec2_instances_with_client(self, instance_ids):
        filters = [{'Name': 'instance-state-name', 'Values' : ["running"]}]
        running_instance_ids_list = [instance.instance_id for instance in self.get_all_ec2_instances(list(instance_ids), filters)]
        response = self.__client.stop_instances(InstanceIds = running_instance_ids_list)
        self.__client_waiter.wait_till_instance_status_stopped(running_instance_ids_list)
        return response
    
    def __stop_ec2_instances_with_resource(self, instance_ids):
        
        filters = [{'Name': 'instance-state-name', 'Values' : ["running"]}]
        running_instance_ids_list = [instance.instance_id for instance in self.get_all_ec2_instances(list(instance_ids), filters)]
        
        running_instances = list(self.__resource.instances.filter(InstanceIds = running_instance_ids_list))
        
        response = self.__resource.instances.filter(InstanceIds = running_instance_ids_list).stop()
        
        for instance in running_instances:
            instance.wait_until_stopped()
            
        return response
 
    
    def __terminate_ec2_instances_with_client(self, instance_ids):
        filters = [{"Name": "instance-state-name", "Values" : ["running", "stopped"]}]
        instance_ids_list = [instance.instance_id for instance in self.get_all_ec2_instances(list(instance_ids), filters)]
        response = self.__client.terminate_instances(InstanceIds = instance_ids_list)
        self.__client_waiter.wait_till_instance_status_terminated(instance_ids_list)
        return response

    def __terminate_ec2_instances_with_resource(self, instance_ids):
        filters = [{"Name": "instance-state-name", "Values" : ["running", "stopped"]}]
        instance_ids_list = [instance.instance_id for instance in self.get_all_ec2_instances(list(instance_ids), filters)]
        instances = list(self.__resource.instances.filter(InstanceIds = instance_ids_list))
        
        response = self.__resource.instances.filter(InstanceIds = instance_ids_list).terminate()
        
        for instance in instances:
            instance.wait_until_terminated()
            
        return response
                    
    def stop_ec2_instances(self, instance_ids):
        """Stops a single or multiple instances using both client and resource AWS object

        Raises:
            AttributeError: when AWS resource or client object is not set for EC2 object...

        Returns:
            json response of the ec2 instances
        """
        print("Stopping instances : {}...".format(','.join(instance_ids)))
        if self.__client:
            return self.__stop_ec2_instances_with_client(instance_ids)
        elif self.__resource:
            return self.__stop_ec2_instances_with_resource(instance_ids)
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def start_ec2_instances(self, instance_ids):
        """Starts a single or multiple instances using both client and resource AWS object

        Raises:
            AttributeError: when AWS resource or client object is not set for EC2 object..

        Returns:
            json response of the ec2 instances
        """
        print("Starting instances : {}...".format(','.join(instance_ids)))
        if self.__client:
            return self.__start_ec2_instances_with_client(instance_ids)
        elif self.__resource:
            return self.__start_ec2_instances_with_resource(instance_ids)
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def terminate_ec2_instances(self, instance_ids):
        """Terminates a single or multiple instances using both client and resource AWS object

        Raises:
            AttributeError: when AWS resource or client object is not set for EC2 object..

        Returns:
            json response of the ec2 instances
        """
        print("Terminating instances : {}...".format(','.join(instance_ids)))
        if self.__client:
            return self.__terminate_ec2_instances_with_client(instance_ids)
        elif self.__resource:
            return self.__terminate_ec2_instances_with_resource(instance_ids)
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
        
    def __get_all_ec2_instances_with_resource(self, instance_ids, filters):
        """Returns all the instances using the AWS resource object

        Yields:
            Instance Ids
        """
        instances = self.__resource.instances.filter(InstanceIds = list(instance_ids), Filters = filters)
            
        for instance in instances:
            yield EC2Instance(instance.instance_id,
                            instance.launch_time,
                            instance.instance_type,
                            instance.platform,
                            instance.image_id,
                            instance.public_ip_address,
                            instance.public_dns_name,
                            instance.private_ip_address,
                            instance.private_dns_name,
                            instance.state.get("Name"), 
                            instance.subnet_id,
                            instance.vpc_id,
                            instance.architecture,
                            instance.instance_lifecycle,
                            [volume.volume_id for volume in instance.volumes.all()]
            );
    
    def __get_all_ec2_instances_with_client(self, instance_ids, filters ):
        """Returns all the instances using the AWS client object

        Yields:
            iterator of EC2Instance objects
        """
        instances_response = self.__client.describe_instances(InstanceIds=list(instance_ids), Filters = filters)
            
        for reservation in instances_response.get("Reservations"):
            for instance in  reservation.get("Instances"):
                yield EC2Instance(instance.get("InstanceId"),
                                instance.get("LaunchTime"), 
                                instance.get("InstanceType"),
                                instance.get("Platform"), 
                                instance.get("ImageId"),
                                instance.get("PublicIpAddress"), 
                                instance.get("PublicDnsName"), 
                                instance.get("PrivateIpAddress"), 
                                instance.get("PrivateDnsName"), 
                                instance.get("State").get("Name"), 
                                instance.get("SubnetId"), 
                                instance.get("VpcId"), 
                                instance.get("Architecture"), 
                                instance.get("InstanceLifecycle"),
                                [volume.get("Ebs").get("VolumeId") for volume in instance.get("BlockDeviceMappings")]
                                
                    );

    def get_all_ec2_instances(self, instance_ids = [], filters = []):
        """Returns all the instances Ids

        Yields:
            Instance Ids
        """
        if self.__resource:
            return self.__get_all_ec2_instances_with_resource(instance_ids, filters);
        elif self.__client:
            return self.__get_all_ec2_instances_with_client(instance_ids, filters);
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
        
    def get_region_available_for_ec2_service(self):
        """It will return all the available regions where ec2 service is avialable

        Raises:
            AttributeError: [description]

        Yields:
            [type]: [description]
        """
        if self.__resource:
            client = self.__resource.meta.client
        elif self.__client:
            client = self.__client
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
        
        for region_response in client.describe_regions().get('Regions'):
            yield ServiceRegion(region_response.get("RegionName"), region_response.get("Endpoint"))
            
        
