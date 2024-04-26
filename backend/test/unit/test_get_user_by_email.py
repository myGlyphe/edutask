import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController, DAO

# list of test case users
USERS = [
    {"firstName": "Jane", "lastName": "Doe", "email": "jane.doe@gmail.com"},
    {"firstName": "John", "lastName": "Doe", "email": "john@gmail.com"},
    {"firstName": "John", "lastName": "Poe", "email": "john@gmail.com"},
]


# test cases for UserController
# test getting valid user by email
@pytest.mark.unit
def test_get_user_by_email_unique():
    mockedDAO = Mock(spec=DAO)
    mockedDAO.find.return_value = [USERS[0]]
    mockedsut = UserController(dao=mockedDAO)
    validationresult = mockedsut.get_user_by_email("jane.doe@gmail.com")
    assert validationresult == USERS[0]


# test duplicate valid emails
@pytest.mark.unit
def test_get_user_by_email_valid_duplicates(capfd):
    dao_mock = Mock(spec=DAO)
    dao_mock.find.return_value = [
        {"email": "duplicate@example.com", "name": "User 1"},
        {"email": "duplicate@example.com", "name": "User 2"},
    ]
    mocked_controller = UserController(dao_mock)
    user = mocked_controller.get_user_by_email("duplicate@example.com")
    assert user == {"email": "duplicate@example.com", "name": "User 1"}


# test duplicate email printed message
@pytest.mark.unit
def test_get_user_by_email_valid_duplicates_message(capfd):
    dao_mock = Mock(spec=DAO)
    dao_mock.find.return_value = [
        {"email": "duplicate@example.com", "name": "User 1"},
        {"email": "duplicate@example.com", "name": "User 2"},
    ]
    mocked_controller = UserController(dao_mock)
    mocked_controller.get_user_by_email("duplicate@example.com")
    output, _ = capfd.readouterr()
    assert "Error: more than one user found with mail duplicate@example.com" in output


# test invalid email
@pytest.mark.unit
def test_get_user_by_email_invalid_email():
    dao_mock = Mock(spec=DAO)
    mocked_controller = UserController(dao_mock)

    with pytest.raises(ValueError) as e_info:
        user = mocked_controller.get_user_by_email("invalidemail")
    assert "Error: invalid email address" in str(e_info.value)


# test invalid email with @ symbol
@pytest.mark.unit
def test_get_user_by_email_invalid_email2():
    mockedDAO = Mock(spec=DAO)
    mockedDAO.find.return_value = []
    mockedsut = UserController(dao=mockedDAO)
    with pytest.raises(ValueError) as e_info:
        user = mockedsut.get_user_by_email("invalid@email")
    assert "Error: invalid email address" in str(e_info.value)


# test nonexistent email
@pytest.mark.unit
def test_get_user_by_email_notfound():
    mockedDAO = Mock(spec=DAO)
    mockedDAO.find.return_value = []
    mockedsut = UserController(dao=mockedDAO)
    validationresult = mockedsut.get_user_by_email("not.found@gmail.com")
    assert validationresult == None


# test database exception
@pytest.mark.unit
def test_get_user_by_email_database_exception():
    dao_mock = Mock(spec=DAO)
    dao_mock.find.side_effect = Exception("Database error")
    mocked_controller = UserController(dao_mock)
    
    with pytest.raises(Exception) as e_info:
        user = mocked_controller.get_user_by_email("test@example.com")
    assert "Database error" in str(e_info.value)
