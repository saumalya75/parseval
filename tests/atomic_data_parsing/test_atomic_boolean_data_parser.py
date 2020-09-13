import pytest
from parseval.parser import BooleanParser
from parseval.exceptions import BooleanParsingException


# Valid value tests type converted
@pytest.mark.parametrize("input_data, expected_output", [
    ('True', True),
    ('fAlSe', False),
    ('T', True),
    ('F', False),
    ('Y', True),
    ('N', False),
    ('yES', True),
    ('No', False),
    (1, True),
    (1.9, True),
    (-2, True),
    (0, False),
    (0.0, False),
    (True, True),
    (False, False)
])
def test_expected_output_type_converted(input_data, expected_output):
    func = BooleanParser().build()
    assert func(input_data) == expected_output


# Valid value tests type preserved
@pytest.mark.parametrize("input_data", ['True', 'fAlSe', 'T', 'F', 'Y', 'N', 'yES', 'No',
                                        1, 1.9, -2, 0, 0.0, True, False])
def test_expected_output_type_preserved(input_data):
    func = BooleanParser(enforce_type=False).build()
    assert func(input_data) == input_data


def test_bad_input():
    func = BooleanParser().build()
    with pytest.raises(BooleanParsingException):
        assert func("anything else")
