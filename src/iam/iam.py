import boto3
import logging

class IAMUser:
    def __init__(self, user_id, user_name=None, arn=None, create_date=None, password_last_used=None, tags=None,
                 path=None):
        self.user_id = user_id
        self.user_name = user_name
        self.arn = arn
        self.create_date = create_date
        self.password_last_used = password_last_used
        self.tags = tags
        self.path = path

    def __str__(self):
        return """IAMUser : [ user_id = {}, user_name = {}, arn = {}, create_date = {}, password_last_used = {}, tags = {}, path = {}] """.format(
            self.user_id,
            self.user_name,
            self.arn,
            self.create_date,
            self.password_last_used,
            self.tags,
            self.path
        )


class IAMGroup:

    def __init__(self, group_id, group_name=None, path=None, arn=None, create_date=None, iam_users=None):
        self.group_id = group_id
        self.group_name = group_name
        self.path = path
        self.arn = arn
        self.create_date = create_date
        self.iam_users = iam_users

    def __str__(self):
        iam_users = "\n\t\t ".join([user.__str__() for user in self.iam_users])
        return """Group Details : [
         group_id = {},
         group_name = {},
         path = {},
         arn = {},
         create_date = {}
         Users :[
         {}
         ]
        ]
         """.format(self.group_id, self.group_name, self.path, self.arn, self.create_date, iam_users)


class IAMService:

    def set_client(self, client_service):
        """It will set the AWS client for IAM

        Args:
            client (AWS client)

        Returns:
            IAM: returns the object of type 
        """
        self.__client = client_service.get_client()
        self.__resource = None
        return self

    def set_resource(self, resource_service):
        """It will set the AWS resource for IAM

        Args:
            client (AWS resource)

        Returns:
            IAM: returns the object of type 
        """

        self.__client = None
        self.__resource = resource_service.get_resource()
        return self

    def __get_users_with_resource(self, user_names):
        """It returns all the IAM user usning IAM resource

        Yields:
            str : name of IAM user
        """
        users = []

        if user_names:
            users = [self.__resource.User(user_name) for user_name in user_names]
        else:
            users = self.__resource.users.all()

        for user in users:
            yield IAMUser(user.user_id,
                          user.user_name,
                          user.arn,
                          user.create_date,
                          user.password_last_used,
                          user.tags,
                          user.path
                          )

    def __get_users_with_client(self, user_names):
        """It returns all the IAM user usning IAM resource

        Yields:
            str : name of IAM user
        """
        users_response = []

        if user_names:
            users_response = [self.__client.get_user(UserName=user_name).get("User") for user_name in user_names]
        else:
            users_response = self.__client.list_users().get('Users')

        for user in users_response:
            yield IAMUser(user.get("UserId"),
                          user.get("UserName"),
                          user.get("Arn"),
                          user.get("CreateDate"),
                          user.get("PasswordLastUsed"),
                          user.get("Tags"),
                          user.get("Path")
                          )

    def __get_groups_using_resource(self, group_names):
        if group_names:
            try:
                for group_name in group_names:
                    group = self.__resource.Group(group_name)
                    yield IAMGroup(group.group_id,
                                   group.group_name,
                                   group.path,
                                   group.arn,
                                   group.create_date,
                                   list(self.get_users([user.user_name for user in group.users.all()]))
                                   )
            except Exception as e:
                logging.exception(e)
        else:
            for group in self.__resource.groups.all():
                yield IAMGroup(group.group_id,
                               group.group_name,
                               group.path,
                               group.arn,
                               group.create_date,
                               list(self.get_users([user.user_name for user in group.users.all()]))
                               )

    def __get_groups_using_client(self, group_names):
        try:
            if not group_names:
                group_names = [group_response.get("GroupName") for group_response in
                               self.__client.list_groups().get("Groups")]
            for group_name in group_names:
                group_response = self.__client.get_group(GroupName=group_name).get('Group')
                users_response = self.__client.get_group(GroupName=group_name).get('Users')
                yield IAMGroup(group_response.get("GroupId"),
                               group_response.get("GroupName"),
                               group_response.get("Path"),
                               group_response.get("Arn"),
                               group_response.get("CreateDate"),
                               list(self.get_users([user_response.get("UserName") for user_response in users_response]))
                               )
        except Exception as e:
            logging.exception(e)

    def get_users(self, user_names=[]):
        """It returns all the IAM user

        Yields:
            str : name of IAM user
        """
        if self.__resource:
            return self.__get_users_with_resource(user_names)
        elif self.__client:
            return self.__get_users_with_client(user_names)
        else:
            raise AttributeError("AWS resource or client object is not set for IAM object")

    def get_groups(self, group_names=[]):
        """
        @summary It will return all groups or some groups with matching filter
        @rtype: IAMGroup object
        @param group_names: List
        """

        if self.__client:
            yield from self.__get_groups_using_client(group_names)

        elif self.__resource:
            yield from self.__get_groups_using_resource(group_names)
        else:
            raise AttributeError("AWS resource or client object is not set for IAM object")
