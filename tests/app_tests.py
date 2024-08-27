from core.repository.UserRepository import get_user_by_id
from database.db import get_session


def test_get_user_1():
    assert 1 == 1