
class EC2:
    def set_client(self, client):
        """It will set the AWS client for IAM

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = client;
        self.__resource = None;
        return self;
    
    def set_resource(self, resource):
        """It will set the AWS resource for IAM

        Args:
            client (AWS resource)

        Returns:
            IAM: returns the object of type 
        """

        self.__client = None;
        self.__resource = resource;
        return self;
    
    def create_key_pair(self, key_name):
        print("Creating a keypair with name : {}".format(key_name))
        if self.__client:
            return self.__client.create_key_pair(
                KeyName = key_name
            )
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def create_security_group(self, group_name, description, vpc_id):
        print("Creating security group with name {} for vpc {}...".format(group_name, vpc_id))
        if self.__client:
            return self.__client.create_security_group(
                GroupName = group_name, 
                Description = description, 
                VpcId = vpc_id
            )
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
            return self._client.run_instances(
                ImageId = image_id,
                InstanceType = instance_type,
                KeyName = key_name,
                MinCount = min_count,
                MaxCount = max_count,
                SecurityGroupIds = [security_group_id],
                SubnetId = subnet_id,
                UserData = user_data     
            )
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
    
    def stop_ec2_instances(self, *instance_ids):
        print("Stopping instances : {}...".format(','.join(instance_ids)))
        if self.__client:
            return self.__client.stop_instances(InstanceIds = list(instance_ids))
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def start_ec2_instances(self, *instance_ids):
        print("Starting instances : {}...".format(','.join(instance_ids)))
        if self.__client:
            return self.__client.start_instances(InstanceIds = list(instance_ids))
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
    
    def terminate_ec2_instances(self, *instance_ids):
        print("Terminating instances : {}...".format(','.join(instance_ids)))
        if self.__client:
            return self.__client.terminate_instances(InstanceIds = list(instance_ids))
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
        
    def __get_all_ec2_instance_ids_with_resource(self):
        """Returns all the instances using the AWS resource object

        Yields:
            Instance Ids
        """
        for instance in self.__resource.instances.all():
            yield instance.instance_id
    
    def __get_all_ec2_instance_ids_with_client(self):
        """Returns all the instances using the AWS client object

        Yields:
            Instance Ids
        """
        for reservation in self.__client.describe_instances().get("Reservations"):
            for instance in  reservation.get("Instances"):
                yield instance.get("InstanceId");
    
    def get_all_ec2_instance_ids(self):
        """Returns all the instances Ids

        Yields:
            Instance Ids
        """
        if self.__resource:
            return self.__get_all_ec2_instance_ids_with_resource();
        elif self.__client:
            return self.__get_all_ec2_instance_ids_with_client();
        else:
            raise AttributeError("AWS resource or client object is not set for EC2 object..")
            
        
