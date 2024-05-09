import random
import string
class Token:
    def set_and_get_token(self):
        return  "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
