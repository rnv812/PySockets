from storage import Storage, UserAlreadyExists


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
        assert isinstance(e, UserAlreadyExists)


def test_get_user_balance():
    balance = storage.get_balance('testname')
    print(type(balance))
    print(balance)
    assert balance == 0


def test_update_user_balance():
    storage.update_balance('testname', 20)
    balance = storage.get_balance('testname')
    assert balance == 20

    storage.update_balance('testname', balance + 30)
    balance = storage.get_balance('testname')
    assert balance == 50

    storage.update_balance('testname', balance - 10)
    balance = storage.get_balance('testname')
    assert balance == 40


def test_delete_user():
    storage.delete_user('testname')
    assert not storage.authenticate('testname', 'password')
