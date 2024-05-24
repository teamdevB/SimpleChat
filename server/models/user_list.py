from server.models.user import User


class UserList:

    def __init__(self):
        self.guest_users = []
        self.host_user = None

    def add_user(self, user_name):
        # userがいない場合
        if self.host_user is None:
            self.host_user = User(user_name=user_name)
        else:
            self.guest_users.append(User(user_name=user_name))

    def get_host_user(self):
        return self.host_user

    def get_guest_users(self):
        return self.guest_users

    def get_guest_user(self, user_name):
        for guest_user in self.guest_users:
            if guest_user.user_name == user_name:
                return guest_user
        return None

    def delete_guest_user(self):
        pass

    def delete_host_user(self):
        pass
