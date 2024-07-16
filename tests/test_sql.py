import pytest
import login
import psycopg2

def test_register():
    assert login.register("test_user", "test_pw", "test@email.com")
    with pytest.raises(psycopg2.Error):
        login.register("test_user", "test_pw", "test@email.com")
