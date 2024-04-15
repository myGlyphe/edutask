import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController, DAO

# regex for email validation
emailValidator = r".+"

# test cases for UserController

# test getting valid user by email
@pytest.mark.unit
def test_get_user_by_email_valid_email_single_user():
    dao_mock = Mock(spec=DAO)
    dao_mock.find.return_value = [{'email': 'test@example.com', 'name': 'Test User'}]
    mocked_controller = UserController(dao_mock)
    user = mocked_controller.get_user_by_email('test@example.com')
    assert user == {'email': 'test@example.com', 'name': 'Test User'}

# test duplicate valid emails
@pytest.mark.unit
def test_get_user_by_email_valid_email_multiple_users(capfd):
    dao_mock = Mock(spec=DAO)
    dao_mock.find.return_value = [{'email': 'duplicate@example.com', 'name': 'User 1'}, {'email': 'duplicate@example.com', 'name': 'User 2'}]
    mocked_controller = UserController(dao_mock)
    user = mocked_controller.get_user_by_email('duplicate@example.com')
    
    output, _ = capfd.readouterr()
    assert user == {'email': 'duplicate@example.com', 'name': 'User 1'}
    assert "Error: more than one user found with mail duplicate@example.com" in output

# test invalid email
@pytest.mark.unit
def test_get_user_by_email_invalid_email():
    dao_mock = Mock(spec=DAO)
    mocked_controller = UserController(dao_mock)
    with pytest.raises(ValueError) as e_info:
        user = mocked_controller.get_user_by_email('invalidemail')
    assert "Error: invalid email address" in str(e_info.value)

# test empty email
@pytest.mark.unit
def test_get_user_by_email_empty_email():
    dao_mock = Mock(spec=DAO)
    mocked_controller = UserController(dao_mock)
    with pytest.raises(ValueError) as e_info:
        user = mocked_controller.get_user_by_email('')
    assert "Error: invalid email address" in str(e_info.value)

# test nonexistent email
@pytest.mark.unit
def test_get_user_by_email_nonexistent_email():
    dao_mock = Mock(spec=DAO)
    dao_mock.find.return_value = []
    mocked_controller = UserController(dao_mock)
    user = mocked_controller.get_user_by_email('nonexistent@example.com')
    assert user is None

# test database exception
@pytest.mark.unit
def test_get_user_by_email_database_exception():
    dao_mock = Mock(spec=DAO)
    dao_mock.find.side_effect = Exception("Database error")
    mocked_controller = UserController(dao_mock)
    with pytest.raises(Exception) as e_info:
        user = mocked_controller.get_user_by_email('test@example.com')
    assert "Database error" in str(e_info.value)
