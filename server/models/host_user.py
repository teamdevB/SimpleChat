## uselsess class
from user import User


class HostUser(User):
    def __init__(self, **info):
        super().__init__(**info)
        self.is_host = True
