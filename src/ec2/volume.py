class Volume:
    def __init__(self, volume_id, volume_type = None, iops = None, throughput = None, is_encrypted = None, snapshot_id = None, state = None, create_time = None, availability_zone = None, tags = None):
        self.volume_id = volume_id
        self.volume_type = volume_type
        self.iops = iops
        self.throughput = throughput
        self.is_encrypted = is_encrypted
        self.snapshot_id = snapshot_id
        self.state = state
        self.create_time = create_time
        self.availability_zone = availability_zone
        self.tags = tags
        
    def __str__(self):
        return """Voume details for volume_Id : {}
                volume_type = {}
                iops = {}
                throughput = {}
                is_encrypted = {}
                snapshot_id = {}
                state = {}
                create_time = {}
                availability_zone = {}
                tags = {}""".format(self.volume_id, 
                                                 self.volume_type, 
                                                 self.iops, 
                                                 self.throughput,
                                                 self.is_encrypted, 
                                                 self.snapshot_id, 
                                                 self.state, 
                                                 self.create_time, 
                                                 self.availability_zone,
                                                 self.tags)
        
        
class VolumeService:
    
    def set_client(self, client_service):
        """It will set the AWS client for VolumeService

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = client_service.get_client()
        self.__client_waiter = client_service.get_waiter()
        self.__resource = None
        self.__client_waiter_from_resource_object = None
        
        return self
        
    def set_resource(self, resource_service):
        """It will set the AWS resource for VolumeService

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = None
        self.__client_waiter = None
        self.__resource = resource_service.get_resource()
        self.__client_waiter_from_resource_object = resource_service.get_client_waiter_from_resource_object()
        
        return self
        
    def __get_all_volumes_with_resource(self, volume_ids, filters):
        """It will return all the volumes present in the aws account using resource

        Yields:
            Volume objects
        """
        volumes = self.__resource.volumes.filter(VolumeIds=list(volume_ids), Filters = filters)
        
        for volume in volumes:
            yield Volume(volume.volume_id,
                         volume.volume_type,
                         volume.iops, 
                         volume.throughput, 
                         volume.encrypted,
                         volume.snapshot_id,
                         volume.state,
                         volume.create_time,
                         volume.availability_zone,
                         volume.tags)
            
    def __get_all_volumes_with_client(self, volume_ids, filters):
        """It will return all the volumes present in the aws account using client

        Yields:
            Volume objects
        """
        volumes = self.__client.describe_volumes(VolumeIds=list(volume_ids), Filters = filters)
        
            
        for volume in volumes.get("Volumes"):
            yield Volume(volume.get("VolumeId"),
                         volume.get("VolumeType"),
                         volume.get("Iops"), 
                         volume.get("Throughput"), 
                         volume.get("Encrypted"),
                         volume.get("SnapshotId"),
                         volume.get("State"),
                         volume.get("CreateTime"),
                         volume.get("AvailabilityZone"), 
                         volume.get("Tags"))
            
    def get_all_volumes(self, volume_ids = [], filters = []):
        """It will return all the volumes present in the aws account

        Raises:
            AttributeError: When AWS resource or client object is not set for VolumeService object

        Returns:
            iterator of type volume 
        """
        if self.__client:
            return self.__get_all_volumes_with_client(volume_ids, filters)
        elif self.__resource:
            return self.__get_all_volumes_with_resource(volume_ids, filters)
        else:
            raise AttributeError("AWS resource or client object is not set for VolumeService object..")
         
    def get_unused_volumes(self, volume_ids = []):
        """It will return the volums which are un used

        Args:
            volume_ids (list, optional):  Defaults to [].

        Returns:
            volume [Volume]
        """
        filters = [{"Name": "status", "Values" : ["available"]}]
        return self.get_all_volumes(volume_ids, filters) 

    def get_unused_untagged_volumes(self, volume_ids = []):
        """It will return the volums which are un used

        Args:
            volume_ids (list, optional):  Defaults to [].

        Returns:
            volume [Volume]
        """
        return [volume for volume in self.get_unused_volumes(volume_ids) if  volume.tags is None] 
    
    def __delete_unused_untagged_volumes_with_client(self, volume_ids):
        for volume_id in volume_ids:
                self.__client.delete_volume(VolumeId = volume_id )
            
        self.__client_waiter.wait_till_volume_deleted(volume_ids)
        
    def __delete_unused_untagged_volumes_with_resource(self, volume_ids):
        for volume in self.get_unused_untagged_volumes(volume_ids):
                self.__resource.Volume(volume.volume_id).delete()
            
        self.__client_waiter_from_resource_object.wait_till_volume_deleted(volume_ids)
    
    def delete_unused_untagged_volumes(self,volume_ids = [] ):
        """It will delete the unused untagged volumes

        Args:
            volume_ids (list, optional): [volume_ids to delete]. Defaults to [].
        """

        volume_ids = [volume.volume_id for volume in self.get_unused_untagged_volumes(volume_ids)]
        if self.__client:
            self.__delete_unused_untagged_volumes_with_client(volume_ids)
            
        elif self.__resource:
            self.__delete_unused_untagged_volumes_with_resource(volume_ids)
        
        else:
            AttributeError("AWS resource or client object is not set for VolumeService object..")
                