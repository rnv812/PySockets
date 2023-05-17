from sqlite3 import IntegrityError

from storage import Storage


storage = Storage()


def test_create_user():
    storage.create_user('testname', 'password')


def test_authenticate_user():
    assert storage.authenticate('testname', 'password')


def test_authenticate_wrong_username():
    assert not storage.authenticate('fakename', 'password')


def test_authenticate_wrong_password():
    assert not storage.authenticate('testname', 'wrongpassword')


def test_duplicate_user():
    try:
        storage.create_user('testname', 'password')
        assert False
    except Exception as e:
        assert isinstance(e, IntegrityError)


def test_delete_user():
    storage.delete_user('testname')
    assert not storage.authenticate('testname', 'password')
