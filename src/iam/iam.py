

class IAM:    
               
    def set_client(self, client_service):
        """It will set the AWS client for IAM

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = client_service.get_client();
        self.__resource = None;
        return self;
    
    def set_resource(self, resource_service):
        """It will set the AWS resource for IAM

        Args:
            client (AWS resource)

        Returns:
            IAM: returns the object of type 
        """

        self.__client = None;
        self.__resource = resource_service.get_resource();
        return self;
    
    def __get_all_users_with_resource(self):
        """It returns all the IAM user usning IAM resource

        Yields:
            str : name of IAM user
        """
        for user in self.__resource.users.all():
                yield user.user_name

    def __get_all_users_with_client(self):
        """It returns all the IAM user usning IAM resource

        Yields:
            str : name of IAM user
        """
        for user in self.__client.list_users().get('Users'):
            yield user.get('UserName')

    
    def get_all_users(self):
        """It returns all the IAM user

        Yields:
            str : name of IAM user
        """
        if self.__resource:
            return self.__get_all_users_with_resource();
        elif self.__client:
            return self.__get_all_users_with_client();
        else:
            raise AttributeError("AWS resource or client object is not set for IAM object")
    

                
    
    
