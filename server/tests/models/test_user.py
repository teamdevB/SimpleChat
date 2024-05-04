import pytest
from server.models.user import User


def test_user_init():
    user_name = 'atsushi'
    assert user_name == 'atsushi'
