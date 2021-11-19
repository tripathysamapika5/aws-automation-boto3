

class S3:    
               
    def set_client(self, client):
        
        """It will set the AWS client for S3

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = client;
        self.__resource = None;
        return self;
    
    def set_resource(self, resource):
        
        """It will set the AWS resource for S3

        Args:
            client (AWS resource)

        Returns:
            IAM: returns the object of type 
        """

        self.__client = None;
        self.__resource = resource;
        return self;
    
    def __get_all_buckets_with_resource(self):
        """It returns all the S3 buckets with aws resource

        Yields:
            str : name of S3 bucket
        """
        for bucket in self.__resource.buckets.all():
                yield bucket.name

    def __get_all_buckets_with_client(self):
        """It returns all the S3 buckets with aws client

        Yields:
            str : name of S3 bucket
        """        
        for bucket in self.__client.list_buckets().get('Buckets'):
            yield bucket.get("Name")

   
    def get_all_buckets(self):
        
        """It returns all the S3 buckets

        Yields:
            str : name of S3 bucket
        """
        if self.__resource:
            return self.__get_all_buckets_with_resource()
        elif self.__client:
            return self.__get_all_buckets_with_client()
        else:
            raise AttributeError("AWS resource or client object is not set for S3 object")
    

                
    
    
