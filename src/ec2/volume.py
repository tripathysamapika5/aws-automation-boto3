class Volume:
    def __init__(self, volume_id, volume_type = None, iops = None, throughput = None, is_encrypted = None, snapshot_id = None, state = None, create_time = None, availability_zone = None):
        self.volume_id = volume_id
        self.volume_type = volume_type
        self.iops = iops
        self.throughput = throughput
        self.is_encrypted = is_encrypted
        self.snapshot_id = snapshot_id
        self.state = state
        self.create_time = create_time
        self.availability_zone = availability_zone
        
    def __str__(self):
        return """Voume details for volume_Id : {}
                volume_type = {}
                iops = {}
                throughput = {}
                is_encrypted = {}
                snapshot_id = {}
                state = {}
                create_time = {}
                availability_zone = {}""".format(self.volume_id, 
                                                 self.volume_type, 
                                                 self.iops, 
                                                 self.throughput,
                                                 self.is_encrypted, 
                                                 self.snapshot_id, 
                                                 self.state, 
                                                 self.create_time, 
                                                 self.availability_zone)
        
        
class VolumeService:
    
    def set_client(self, client_service):
        """It will set the AWS client for VolumeService

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = client_service.get_client()
        self.__resource = None
        return self
        
    def set_resource(self, resource_service):
        """It will set the AWS resource for VolumeService

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = None
        self.__resource = resource_service.get_resource()
        return self
        
    def __get_all_volumes_with_resource(self):
        """It will return all the volumes present in the aws account using resource

        Yields:
            Volume objects
        """
        for volume in self.__resource.volumes.all():
            yield Volume(volume.volume_id,
                         volume.volume_type,
                         volume.iops, 
                         volume.throughput, 
                         volume.encrypted,
                         volume.snapshot_id,
                         volume.state,
                         volume.create_time,
                         volume.availability_zone)
            
    def __get_all_volumes_with_client(self):
        """It will return all the volumes present in the aws account using client

        Yields:
            Volume objects
        """
        for volume in self.__client.describe_volumes().get("Volumes"):
            yield Volume(volume.get("VolumeId"),
                         volume.get("VolumeType"),
                         volume.get("Iops"), 
                         volume.get("Throughput"), 
                         volume.get("Encrypted"),
                         volume.get("SnapshotId"),
                         volume.get("State"),
                         volume.get("CreateTime"),
                         volume.get("AvailabilityZone"))
            
    def get_all_volumes(self):
        """It will return all the volumes present in the aws account

        Raises:
            AttributeError: When AWS resource or client object is not set for VolumeService object

        Returns:
            iterator of type volume 
        """
        if self.__client:
            return self.__get_all_volumes_with_client()
        elif self.__resource:
            return self.__get_all_volumes_with_resource()
        else:
            raise AttributeError("AWS resource or client object is not set for VolumeService object..")
         