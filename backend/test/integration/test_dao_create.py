import pytest
from unittest.mock import patch
from pymongo.errors import WriteError

from src.util.dao import DAO
from src.util.validators import getValidator

valid_documents = {
    'user': {
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'jane.doe@gmail.com'
    },

    'task': {
        'title': 'Improve Devtools',
        'description': 'Upgrade the tools'
    },

    'todo': {
        'description': 'Watch video'
    },

    'video': {
        'url': 'U_gANjtv28g'
    }
}

invalid_documents = {
    'user': {
        'firstName': 'Jane',
        'lastName': 'Doe'
    },

    'task': {
        'title': 'Improve Devtools',
        'description': 'Upgrade the tools',
        'video': 'U_gANjtv28g'
    },

    'todo': {
        'description': 'Watch video',
        'done': 'True'
    },

    'video': {
        'url': ['U_gANjtv28g']
    }
}

@pytest.fixture
def sut(test_collection_name):
    """
    The fixture first strips the test_ prefix from the collection name to get the validator name,
    and then retrieves the validator using the getValidator function.

    Then the getValidator function is patched in the DAO initializer (which otherwise would not
    have found the validator with a test_ prefix).

    Finally, the created DAO object, with a correct validator, is returned.
    """
    collection_name = test_collection_name.removeprefix('test_')
    validator = getValidator(collection_name)

    with patch('src.util.dao.getValidator', autospec=True) as mockedgetValidator:
        mockedgetValidator.return_value = validator
        sut = DAO(test_collection_name)
        yield sut

        # Remove the temporary test collection when the test has been concluded
        sut.drop()

@pytest.mark.integration
@pytest.mark.parametrize('test_collection_name, document_key', [
    ('test_user', 'user'),
    ('test_task', 'task'),
    ('test_todo', 'todo'),
    ('test_video', 'video')])
def test_create_valid(sut, document_key):
    """
    Check that it is possible to create valid documents with the required properites.
    """
    document = valid_documents[document_key]
    created = sut.create(document)

    # Remove the generated _id key before comparison
    del created['_id']
    assert document == created

@pytest.mark.integration
@pytest.mark.parametrize('test_collection_name, document_key', [
    ('test_user', 'user'),
    ('test_task', 'task'),
    ('test_todo', 'todo'),
    ('test_video', 'video')])
def test_create_invalid(sut, document_key):
    """
    Check that a WriteError is raised when trying to create a document that does not
    conform to the validator.
    """
    document = invalid_documents[document_key]

    with pytest.raises(WriteError):
        created = sut.create(document)

