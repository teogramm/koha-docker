import random
import string

import pytest


@pytest.fixture(scope="session")
def database_credentials() -> tuple[str,str]:
    """
    Randomly generates a username and a password for the database
    :return: tuple containing username, password
    """
    username_length = 5
    username = ''.join(random.choices(string.ascii_lowercase, k=username_length))
    password_length = 8
    password = ''.join(random.choices(string.ascii_lowercase, k=password_length))
    return str(username), str(password)
