import pprint
import tempfile
import datetime
from parseval.parser import Parser
from parseval.parser import (
    StringParser,
    DatetimeParser,
    IntegerParser,
    FloatParser,
    ConstantParser
)
# Here instead of using parsers on only atomic values, we will use built-in `Parser` class to process dataset
# Parser class can handle multiple types of dataset like file object, list of lines, list of jsons etc
# It can produce output data in multiple format also. For all details please checkout the documentation.
# For demo purposes we will consider input in file object, and the parsed rows will be returned in JSON format
# Note, directly passing file name is not supported yet, in pipeline for future version
# Note, the parser API will yield a generator as output.

# To process any kind of dataset, first one schema has to be defined
# Schema is nothing but a set of parsers, stored in a specific structure in the sequence of columns in dataset


# Some custom validation
def _parity_check(data):
    if data:
        try:
            i_Data = int(data)
        except:
            pass
        if i_Data % 2 != 0:
            raise Exception("The data has to be even!")
    return data


# The cursors has to provided in a list, where each element of the list is a tuple.
# First element of each element is the column name, this is just for reference, no internal usage
# Second element of each tuple is the actual parser (parser objects, not built parser function)
schema = [
    ('ID', StringParser(quoted=1)),
    ('RUN_ID', StringParser().regex_match(r'\w+_\d{4}-\d{2}-\d{2}').change_case('u')),
    ('CLASS', StringParser(start=1, end=1).value_set(['a', 'b', 'A'])),
    ('INITIATED_ON', DatetimeParser(formats=['%Y%m%d', '%Y-%m-%d %H:%M:%S']).convert('%Y/%m/%d').max_value(datetime.datetime.now()).min_value(value='20000101', format='%Y%m%d').not_null(datetime.datetime.strptime('19001231', '%Y%m%d'))),
    ('ASKED_AMOUNT', IntegerParser().max_value(2000).not_null(default_value=0)),
    ('ADJUSTED_AMOUNT', FloatParser().min_value(10.0).not_null(0.0)),
    ('ROLE_MODEL', ConstantParser('Iron-Man')),
    ('BLOCK_NUMBER', IntegerParser().add_func(_parity_check).range(0, 40))
]

p = Parser(schema=schema, stop_on_error=1, parsed_row_format='json')
# Creating temporary file for the example
with tempfile.NamedTemporaryFile() as tf:
    with open(tf.name, 'w') as sf:
        sf.writelines('""|Trig2020-23-12|A|20200123|2000|21.0934||10\n')
        sf.writelines('"DEF"||abc|||||34\n')
        sf.writelines('"DEF"|Manual_2020-23-12||2020-01-23 10:20:23|1200|11||')

    print('#' * 50, " DATASET PARSING ", '#' * 50)
    parsed_lines = []
    with open(tf.name, 'r') as sf:
        for parsed_line in p.parse(sf):  # calling data parsing on file object
            parsed_lines.append(parsed_line)
    print("\n\n>>> Parsed Data:")
    pprint.pprint(parsed_lines)
    print('#' * 125)
