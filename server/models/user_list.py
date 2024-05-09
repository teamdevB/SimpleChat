## uselsess class
from user import User


class UserList(User):
    def __init__(self) :
        self.user_list = []
        super().__init__()
    def add_user(self,user):
        self.user_list.append(user)
    def remove_user(self,user):
        self.user_list.remove(user)
    def get_user_list(self):
        return self.user_list
    def get_user_list_length(self):
        return len(self.user_list)


