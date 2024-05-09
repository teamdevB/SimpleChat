## uselsess class
from user import User


class GuestUser(User):
    def __init__(self, **info):
        super().__init__(**info)
        self.is_host = False

