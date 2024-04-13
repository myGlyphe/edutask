import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

USERS = [
    {
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'jane.doe@gmail.com'
    },
    {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john@gmail.com'
    },
    {
        'firstName': 'John',
        'lastName': 'Poe',
        'email': 'john@gmail.com'
    }
]

@pytest.mark.unit
def test_get_user_by_email_unique():
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [USERS[0]]
    mockedsut = UserController(dao=mockedDAO)
    validationresult = mockedsut.get_user_by_email('jane.doe@gmail.com')
    assert validationresult == USERS[0]

@pytest.mark.unit
def test_get_user_by_email_nonunique():
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [USERS[1], USERS[2]]
    mockedsut = UserController(dao=mockedDAO)
    validationresult = mockedsut.get_user_by_email('john@gmail.com')
    assert validationresult == USERS[1]

@pytest.mark.unit
def test_get_user_by_email_nonunique_warningmsg(capfd):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [USERS[1], USERS[2]]
    mockedsut = UserController(dao=mockedDAO)
    validationresult = mockedsut.get_user_by_email('john@gmail.com')
    captured = capfd.readouterr()
    assert 'john@gmail.com' in captured.out

@pytest.mark.unit
def test_get_user_by_email_notfound():
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = []
    mockedsut = UserController(dao=mockedDAO)
    validationresult = mockedsut.get_user_by_email('not.found@gmail.com')
    assert validationresult == None

@pytest.mark.unit
def test_get_user_by_email_invalid():
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = []
    mockedsut = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        validationresult = mockedsut.get_user_by_email('invalid@gmail')

@pytest.mark.unit
def test_get_user_by_email_invalid2():
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = []
    mockedsut = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        validationresult = mockedsut.get_user_by_email('invalid_gmail')

