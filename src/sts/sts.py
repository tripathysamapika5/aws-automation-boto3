
class STS:
    
    def __init__(self, client_service):
        self.__client = client_service.get_client()
    
    def get_user_id(self):
        """Returns the user id of the caller(IAM user/root account)

        Returns:
            user_id
        """
        return self.__client.get_caller_identity().get("UserId")
    
    def get_account_id(self):
        """Returns the account id of the caller(IAM user/root account)

        Returns:
            account id
        """
        return self.__client.get_caller_identity().get("Account")
    
    def get_iam_user_arn(self):
        """Returns the arn of the caller(IAM user/root account)

        Returns:
            arn
        """
        return self.__client.get_caller_identity().get("Arn")