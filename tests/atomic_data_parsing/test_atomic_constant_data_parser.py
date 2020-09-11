import pytest
from parseval.parser import ConstantParser


# Valid value tests type preserved
@pytest.mark.parametrize("input_data", ['True', 'fAlSe', 'T', 'F', 'Y', 'N', 'yES', 'No',
                                        1, 1.9, -2, 0, 0.0, True, False, None, ''])
def test_expected_output_type_preserved(input_data):
    func = ConstantParser(value=3).build()
    assert func(input_data) == 3

