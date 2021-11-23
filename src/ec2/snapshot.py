class Snapshot:
    def __init__(self, 
                 snapshot_id, 
                 volume_id, 
                 start_time = None, 
                 is_encrypted = None, 
                 kms_key_id = None, 
                 state = None, 
                 volume_size = None, 
                 tags = None):
        self.snapshot_id = snapshot_id
        self.volume_id = volume_id
        self.start_time = start_time
        self.is_encrypted = is_encrypted
        self.kms_key_id = kms_key_id
        self.state = state
        self.volume_size = volume_size
        self.tags = tags
    

        
    def __str__(self):
        return """Snapshot details for snapshot with id  : {}
                volume_id = {}
                start_time = {}
                is_encrypted = {}
                kms_key_id = {}
                state = {}
                volume_size = {}
                tags = {}""".format(self.snapshot_id, 
                                                 self.volume_id, 
                                                 self.start_time, 
                                                 self.is_encrypted, 
                                                 self.kms_key_id, 
                                                 self.state, 
                                                 self.volume_size,
                                                 self.tags)


class SnapshotService:
    
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
        
    def __get_all_snapshots_with_resource(self, snapshot_ids, filters, owner_ids):
        
        snapshots = self.__resource.snapshots.filter(OwnerIds = owner_ids, SnapshotIds = list(snapshot_ids), Filters = filters)
        
        for snapshot in snapshots:
            yield Snapshot(snapshot.snapshot_id,
                         snapshot.volume_id,
                         snapshot.start_time,
                         snapshot.encrypted,
                         snapshot.kms_key_id, 
                         snapshot.state,
                         snapshot.volume_size,
                         snapshot.tags
                         )
            
    def __get_all_snapshots_with_client(self, snapshot_ids, filters, owner_ids):
        
        snapshots = self.__client.describe_snapshots(OwnerIds = owner_ids, SnapshotIds = list(snapshot_ids), Filters = filters)
        
        for snapshot in snapshots.get("Snapshots"):
            yield Snapshot(snapshot.get("SnapshotId"),
                         snapshot.get("VolumeId"),
                         snapshot.get("StartTime"),
                         snapshot.get("Encrypted"),
                         snapshot.get("KmsKeyId"), 
                         snapshot.get("State"),
                         snapshot.get("VolumeSize"),
                         snapshot.get("Tags")
                         )
            
    def get_all_snapshots(self, snapshot_ids = [], filters = [], owner_ids = ["self"]):
        """It will return all the snapshots present in the aws account

        Raises:
            AttributeError: When AWS resource or client object is not set for SnapshotService object

        Returns:
            iterator of type snapshot 
        """

        if self.__client:
            return self.__get_all_snapshots_with_client(snapshot_ids, filters, owner_ids)
        elif self.__resource:
            return self.__get_all_snapshots_with_resource(snapshot_ids, filters, owner_ids)
        else:
            raise AttributeError("AWS resource or client object is not set for SnapshotService object..")
    
    def get_snapshots_filted_on_volume_size(self,volume_sizes = [], snapshot_ids = [], filters = [], owner_ids = ["self"]):
        volume_sizes = [str(volume_size) for volume_size in volume_sizes]
        filters.append({"Name" : "volume-size", "Values" : volume_sizes})
        
        print(filters)
                    
        return self.get_all_snapshots(snapshot_ids, filters, owner_ids)