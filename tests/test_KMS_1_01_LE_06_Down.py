import pytest
from unittest.mock import patch
from KMS_1_01_LE_06_Down import change_values, PersonData


@pytest.fixture
def sample_person():
    return PersonData("John Doe", "John", "Doe", "Employee", "123 Main St 1234 City", "01.01.1990", "+43123123123", "q@gmail.com")

@pytest.fixture()
def sample_people_data(sample_person):
    return {sample_person.get_name(): sample_people_data}

def test_change_values(sample_person, sample_people_data):
    old = sample_person.get_name()
    with patch('builtins.input', side_effect =["1", "3", "Jane Smith", "7"]):
        change_values(sample_person, sample_people_data)
    if sample_person.get_name != old:
        del sample_people_data[old]
        sample_people_data[sample_person.get_name()] = sample_person
    #test full name change
    assert sample_person.get_name() == "Jane Smith"
    assert "Jane Smith" in sample_people_data
    assert "John Doe" not in sample_people_data
    assert sample_people_data["Jane Smith"] == sample_person

    old = sample_person.get_name()
    with patch('builtins.input', side_effect=["1", "1", "Olli", "7"]):
        change_values(sample_person, sample_people_data)
    if sample_person.get_name != old:
        del sample_people_data[old]
        sample_people_data[sample_person.get_name()] = sample_person
    #change first name
    assert sample_person.get_name() == "Olli Smith"
    assert "Olli Smith" in sample_people_data
    assert "Jane Smith" not in sample_people_data
    assert sample_people_data["Olli Smith"] == sample_person

    old = sample_person.get_name()
    with patch('builtins.input', side_effect = ["1", "2", "Brown", "7"]):
        change_values(sample_person, sample_people_data)
    if sample_person.get_name != old:
        del sample_people_data[old]
        sample_people_data[sample_person.get_name()] = sample_person
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

'''
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