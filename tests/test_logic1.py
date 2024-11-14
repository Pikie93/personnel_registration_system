import pytest
from unittest.mock import patch
from ..logic1 import change_values, write_to
from person_data_class import PersonData


@pytest.fixture
def sample_person():
    return PersonData("John Doe", "John", "Doe", "Employee", "123 Main St 1234 City", "01.01.1990", "+43123123123", "q@gmail.com")

@pytest.fixture
def sample_people_data(sample_person):
    return {sample_person.get_name(): sample_people_data}

@pytest.fixture
def mock_write_to():
    with patch('logic1.write_to') as mock:
        yield mock

@pytest.mark.parametrize("attribute, new_value, expected_result, get_method", [
    ("Full Name", "Jane Smith", "New name is Jane Smith", "get_name"),
    ("First Name", "Olli", "New first name is Olli.", "get_first_name"),
    ("Last Name", "Brown", "New last name is Brown", "get_last_name"),
    ("Status", "Manager", "New status is Manager", "get_status"),
    ("Address", "456 Elm St 5678 Town", "New address is 456 Elm St 5678 Town", "get_address"),
    ("Date of Birth", "02.02.1991", "New date of birth is 02.02.1991", "get_dob"),
    ("Phone Number", "+43987654321", "New phone number is +43987654321", "get_phone_number"),
    ("Email Address", "new@email.com", "New email address is new@email.com", "get_email"),
])

def test_change_values(sample_person, sample_people_data, mock_write_to, attribute, new_value, expected_result, get_method):
    filename = "test_file.json"

    result = change_values(sample_person, attribute, new_value, sample_people_data, filename)
    
    assert result == expected_result
    assert getattr(sample_person, get_method)() == new_value
    
    if attribute in ["Full Name", "First Name", "Last Name"]:
        assert new_value in sample_people_data or new_value.split()[-1] in sample_people_data
    
    mock_write_to.assert_called_with(filename, sample_people_data)

def test_change_values_invalid_input(sample_person, sample_people_data, mock_write_to):
    filename = "test_file.json"
    result = change_values(sample_person, "Full Name", "123 Invalid", sample_people_data, filename)
    assert "Invalid name" in result
    assert sample_person.get_name() == "John Doe"
    mock_write_to.assert_not_called()

@pytest.mark.parametrize("attribute, new_value", [
    ("Status", "InvalidStatus"),
    ("Date of Birth", "InvalidDate"),
    ("Phone Number", "InvalidPhone"),
    ("Email Address", "InvalidEmail"),
])
def test_change_values_invalid_attributes(sample_person, sample_people_data, mock_write_to, attribute, new_value):
    filename = "test_file.json"
    result = change_values(sample_person, attribute, new_value, sample_people_data, filename)
    assert result != f"New {attribute.lower()} is {new_value}"
    mock_write_to.assert_not_called()
    '''
    #Test full name change
    result = change_values(sample_person, "Full Name", "Jane Smith", sample_people_data, filename)
    assert result == "New name is Jane Smith"
    assert "Jane Smith" in sample_people_data
    assert "John Doe" not in sample_people_data
    assert sample_people_data["Jane Smith"] == sample_person

    mock_write_to.assert_called_with(filename, sample_people_data)

    
    #Test first name change
    result =change_values(sample_person, "First Name", "Olli", sample_people_data, filename)
    assert result == "New first name is Olli"
    assert "Olli Smith" in sample_people_data
    assert "Jane Smith" not in sample_people_data
    assert sample_people_data["Olli Smith"] == sample_person

    mock_write_to.assert_called_with(filename, sample_people_data)

    #change last name
    assert sample_person.get_name() == "Olli Brown"
    assert "Olli Brown" in sample_people_data
    assert "Olli Smith" not in sample_people_data
    assert sample_people_data["Olli Brown"] == sample_person

    #test canceling
    with patch('builtins.input', side_effect=["1","6","7"]):
        change_values(sample_person, sample_people_data)

    assert sample_person.get_name() == "Olli Brown"
    assert "Olli Brown" in sample_people_data

    #invalid
    with patch('builtins.input', side_effect=["1", "3" "123 Invalid", "6", "7"]):
        change_values(sample_person, sample_people_data)

    assert sample_person.get_name() == "Olli Brown"
    assert "Olli Brown" in sample_people_data

    #exit
    with patch('builtins.input', return_value="7"):
        result = change_values(sample_person,sample_people_data)

        assert result == "7"
        assert sample_person.get_name() == "Olli Brown"
        assert "Olli Brown" in sample_people_data

    #inv then exit
    with patch('builtins.input', side_effect=["8","7"]):
        change_values(sample_person, sample_people_data)

        assert sample_person.get_name() == "Olli Brown"
        assert "Olli Brown" in sample_people_data


class TestObject:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __str__(self):
        return f"TestObject({self.name}{self.status})"

@pytest.mark.parametrize("inputs,expected", [
    (["1"], "add"),
    (["2"], "redo"),
    (["3"], "exit"),
    (["4", "1"], "add")
])

def test_confirm_info(capsys, monkeypatch, inputs, expected):
    test_obj = TestObject("testname", "teststatus")

    input_iter = iter(inputs)

    monkeypatch.setattr('builtins.input', lambda _: next(input_iter))

    result = confirm_info(test_obj)

    assert result == expected

    captured = capsys.readouterr()

    assert f"TestObject(testnameteststatus)\n" in captured.out'''