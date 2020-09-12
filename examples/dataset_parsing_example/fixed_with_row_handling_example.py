import pprint
from parseval.parser import Parser
from parseval.parser import (
    StringParser,
    IntegerParser,
    FloatParser
)
# In this example we will see how fixed width dataset can be processed using `Parser` API
# For all types of dataset structure, fixed width data is supported
# For demo purposes we will consider input in list of rows format, and the parsed rows will be returned in JSON format

# To process any kind of dataset, first one schema has to be defined
# Schema is nothing but a set of parsers, stored in a specific structure in the sequence of columns in dataset


# The cursors has to provided in a list, where each element of the list is a tuple.
# First element of each element is the column name, this is just for reference, no internal usage
# Second element of each tuple is the actual parser (parser objects, not built parser function)

fw_schema = [
    ('ID', StringParser(1, 2)),
    ('NAME', StringParser(3, 5).change_case('U').not_null('nan', allow_white_space=True)),
    ('GENDER', StringParser(6, 6).value_set(['M', 'F'])),
    ('NOT_NULLABLE_VALUE', StringParser(7, 11).not_null('dummy')),
    ('NULLABLE_VALUE', StringParser(7, 11)),
    ('BIRTH_YEAR', IntegerParser(12, 13).max_value(20)),
    ('BALANCE', FloatParser(14, 17).min_value(10.0))
]
p = Parser(schema=fw_schema, stop_on_error=1, input_row_format='fixed-width', parsed_row_format='json')
print('#' * 50, " FIXED WIDTH DATASET PARSING ", '#' * 50)
parsed_data = p.parse([
    'd0sauMvalue191000',
    'd0pouM     2090.03',
    'd0pouX     2090.03'
])
print("\n\n>>> Parsed Data:")
for data in parsed_data:
    pprint.pprint(data)
print('#' * 125)
