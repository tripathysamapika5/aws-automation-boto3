import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2
from src.aws_resources.client_locator import ClientLocator, EC2Client
from src.utils.utilities import Utilities


def main():
        
    # creating a vpc client
    ec2_client_service = EC2Client()
    vpc = VPC(ec2_client_service)
    
    # Creating utility object
    utility = Utilities()
    
    #Reading config for application
    properties = utility.read_config_properties(env = 'prod', section_name = 'VPC')
 
    
    # creating a vpc
    vpc_response = vpc.create_vpc(properties['vpc.cidr.block'])
    vpc_id = utility.get_value_from_json(vpc_response, 'VpcId')
    print("VPC created with id : {}".format(vpc_id))
    
    # Naming the vpc
    vpc.add_name_tag(vpc_id, properties['vpc.name'])
    print("VPC : {} named as : {}".format(vpc_id, properties['vpc.name']))
    
    # creating internet gateway
    igw_response = vpc.create_internet_gateway()
    igw_id = utility.get_value_from_json(igw_response, 'InternetGatewayId')
    print("IGW created with id : {}".format(igw_id))
    
    # attaching the IGW to VPC
    vpc.attach_igw_to_vpc(igw_id, vpc_id)
    print("IGW {} is attached to VPC {}".format(igw_id, vpc_id))
    
    # creating public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, properties['public.subnet.cidr.block'])
    public_subnet_id = utility.get_value_from_json(public_subnet_response, 'SubnetId')     
    print("Public subnet with id {} created  to VPC {}".format(public_subnet_id, vpc_id))

    # Add a name tag to private subnet
    vpc.add_name_tag(public_subnet_id, properties['public.subnet.name'])
    print("Public subnet : {} named as : {}".format(public_subnet_id,properties['public.subnet.name']))

    # Creating Public Route Table
    public_route_table_response = vpc.create_public_route_table(vpc_id)
    public_route_table_id = utility.get_value_from_json(public_route_table_response, 'RouteTableId')
    print("Route table {} is created to VPC {} ".format(public_route_table_id, vpc_id))
    
    # Creating internet gateway route to public route table
    create_igw_route_response = vpc.create_igw_route_to_public_route_table(
        properties['client.cidr.block'], 
        igw_id, 
        public_route_table_id
    )
    print("created internet gateway route to public route table")

    #Associate public subnet with public route table
    associate_route_table_to_subnet_response = vpc.associate_route_table_to_subnet(public_route_table_id, public_subnet_id)
    print("Associated route table to subnet")


    #Allow auto assign of ip addresses to public subnet
    allow_auto_assign_ip_addresses_for_subnet_response = vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)
    print("Allowed auto assign of ip addresses to public subnet {}".format(public_subnet_id))

    # Creating private subnet
    private_subnet_response = vpc.create_subnet(vpc_id, properties['private.subnet.cidr.block'])
    private_subnet_id = utility.get_value_from_json(private_subnet_response, 'SubnetId')  
    print("Private subnet id {} created  to VPC {} ".format(private_subnet_id, vpc_id))

    # Add a name tag to private subnet
    vpc.add_name_tag(private_subnet_id, properties['private.subnet.name'])
    print("Private subnet : {} named as : {}".format(private_subnet_id,properties['private.subnet.name']))


    
    
    #EC2 instances
    ec2 = EC2().set_client(ec2_client_service)
    
    # creating a keypair
    keypair_response = ec2.create_key_pair(properties['keypair.name'])
    print('Keypair created as : {}'.format(keypair_response))

    # create a public security group
    public_security_group_response = ec2.create_security_group(
        properties['public.security.group.name'],
        properties['public.security.group.description'],
        vpc_id
    )
    public_security_group_id = utility.get_value_from_json(public_security_group_response, 'GroupId')
    print('Public security Group {} is created'.format(public_security_group_id))

    # Adding public acccess to security group
    
    ip_permissions = ec2.create_ip_permission_list_for_inbound_rule(
        properties['tcp.ip.protocol'],
        properties['tcp.source.to.destination.ports'],
        properties['cidr.ip.ranges']
    )

    add_inbound_rule_to_sg_response = ec2.add_inbound_rule_to_sg(
        public_security_group_id, 
        ip_permissions
    )
    print("Security group inbound rule added to {} ".format(public_security_group_id))
    
    #Launching a public EC2 instance
    ec2_public_launch_config = {}
    ec2_public_launch_config['image_id'] = properties.get('ec2.image_id')
    ec2_public_launch_config['instance_type'] = properties.get('ec2.instance.type')
    ec2_public_launch_config['key_name'] = properties.get('keypair.name')
    ec2_public_launch_config['min_count'] = 1
    ec2_public_launch_config['max_count'] = 1
    ec2_public_launch_config['security_group_id'] = public_security_group_id
    ec2_public_launch_config['subnet_id'] = public_subnet_id
    ec2_public_launch_config['user_data'] = utility.read_file_to_string(properties.get('ec2.userdata.filepath'))
    
    launch_ec2_instance_response = ec2.launch_ec2_instance(**ec2_public_launch_config)
    pubic_instance_id = utility.get_value_from_json(launch_ec2_instance_response, 'InstanceId')  
    print("Public EC2 instance : {} got created with AMI : {} ".format(pubic_instance_id, ec2_public_launch_config.get('image_id')))

    # create a private security group
    private_security_group_response = ec2.create_security_group(
        properties['private.security.group.name'],
        properties['private.security.group.description'],
        vpc_id
    )
    private_security_group_id = utility.get_value_from_json(private_security_group_response, 'GroupId')
    print('Private security Group {} is created'.format(private_security_group_id))

    # Adding rule to the private security group
    add_inbound_rule_to_private_sg_response = ec2.add_inbound_rule_to_sg(
        private_security_group_id, 
        ip_permissions
    )
    print("Security group inbound rule added to {} ".format(private_security_group_id))


    #Launching a private EC2 instance
    ec2_private_launch_config = {}
    ec2_private_launch_config['image_id'] = properties.get('ec2.image_id')
    ec2_private_launch_config['instance_type'] = properties.get('ec2.instance.type')
    ec2_private_launch_config['key_name'] = properties.get('keypair.name')
    ec2_private_launch_config['min_count'] = 1
    ec2_private_launch_config['max_count'] = 1
    ec2_private_launch_config['security_group_id'] = private_security_group_id
    ec2_private_launch_config['subnet_id'] = private_subnet_id
    ec2_private_launch_config['user_data'] = ''
    
    launch_private_ec2_instance_response = ec2.launch_ec2_instance(**ec2_private_launch_config)
    private_instance_id = utility.get_value_from_json(launch_private_ec2_instance_response, 'InstanceId')  
    print("Private EC2 instance : {} got created with AMI : {} ".format(private_instance_id, ec2_public_launch_config.get('image_id')))


if __name__ == '__main__':
    main()