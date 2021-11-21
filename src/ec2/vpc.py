
class VPC: 
    def __init__(self, client_service) : 
        self._client = client_service.get_client()
        self.__client_waiter = client_service.get_waiter()
        
    def create_vpc(self, cidr_block):
        print("creating VPC...")
        response = self._client.create_vpc(
            CidrBlock = cidr_block
        )
        
        vpc_id = response.get("Vpc").get("VpcId")
        self.__client_waiter.wait_till_vpc_available([vpc_id])
        return response
        
    def add_name_tag(self,resource_id, resource_name):
        print("Adding name {} to resource with id {}".format(resource_name, resource_id))
        return self._client.create_tags(
            Resources=[resource_id],
            Tags = [{
                'Key' : 'Name',
                'Value' : resource_name
            }]
        )

    def create_internet_gateway(self):
        print("Creating internet gateway...")
        return self._client.create_internet_gateway()
    
    def attach_igw_to_vpc(self, igw_id, vpc_id):
        print("Attaching internet gateway {} to vpc id {}...".format(igw_id, vpc_id))
        return self._client.attach_internet_gateway(InternetGatewayId = igw_id, VpcId = vpc_id)
    
    def create_subnet(self, vpc_id, cidr_block):
        print("Creating a subnet for vpc : {} and cidrBlock : {}...".format(vpc_id, cidr_block))
        response = self._client.create_subnet(
            VpcId = vpc_id, 
            CidrBlock = cidr_block
        )
        subnet_id = response.get("Subnet").get("SubnetId")
        self.__client_waiter.wait_till_subnet_available([subnet_id])
        return response

    def create_public_route_table(self, vpc_id):
        print("Creating Route table for public subnet...")
        return self._client.create_route_table(
            VpcId = vpc_id
        )
        
    def create_igw_route_to_public_route_table(self, destination_cidr_block, igw_id, public_route_table_id):
        print("Creating internet gateway route to public route table...")
        return self._client.create_route(
            DestinationCidrBlock = destination_cidr_block,
            GatewayId = igw_id,
            RouteTableId = public_route_table_id
        )
        
    def associate_route_table_to_subnet(self, route_table_id, subnet_id):
        print("Associate route table to subnet...")
        self._client.associate_route_table(
            RouteTableId = route_table_id,
            SubnetId = subnet_id
        )

    def allow_auto_assign_ip_addresses_for_subnet(self, subnet_id):
        print("Allow auto assign of ip addresses to subnet with id {}...".format(subnet_id))
        return self._client.modify_subnet_attribute(
            MapPublicIpOnLaunch={'Value': True},
            SubnetId=subnet_id
        ) 
                    
    