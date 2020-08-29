# Import required parser class
from parseval.parser import DatetimeParser
import datetime

basic_parser = DatetimeParser(formats=['%Y%m%d'])  # Create basic parser object
basic_parse_func = basic_parser.build()  # Build the parser function
input_data = "20200101"  # Input Data
basic_parsed_output = basic_parse_func(input_data)  # Parse data

print('#' * 50, " DATETIME PARSING ", '#' * 50)
print('====>', "Simple Data Parsing example:")
print("Input 1: {}".format(input_data))
print("Output 1: {}".format(basic_parsed_output))
print('\n')


# Now let's see some available validators, to get the idea of how to use those
# Note, we will not go through all available validators, because all validators work in same fashion
# Syntax and description of all validators are available in documentation
default_date = datetime.datetime.strptime("20200101", "%Y%m%d")
min_date = datetime.datetime.strptime("20200101", "%Y%m%d")
max_date = datetime.datetime.strptime("20200831", "%Y%m%d")
validation_parser = DatetimeParser()\
    .range(min_date, max_date)\
    .not_null(default_value=default_date)  # null check validation and allowed values validation is added
validation_parse_func = validation_parser()  # Yes, you can directly call the object to build the parser

more_generic_parser = DatetimeParser(formats=['%Y%m%d', '%Y%m%d %H%M%S'])  # Create basic parser object
more_generic_parse_func = more_generic_parser.build()  # Build the parser function
valid_input_data = "20200101 090708"
output_for_valid_input_data = more_generic_parse_func(valid_input_data)  # Parse data
print('====>', "Data Validation example:")
print("Input 2: {}".format(valid_input_data))
print("Output 2: {}".format(output_for_valid_input_data))
print('\n')

null_input = None
output_for_null_input = validation_parse_func(null_input)
print("Input 3: {}".format(null_input))
print("Output 3: {}".format(output_for_null_input))
print('\n')

empty_string_input = ""
output_for_empty_string_input = validation_parse_func(empty_string_input)
print("Input 4: {}".format(empty_string_input))
print("Output 4: {}".format(output_for_empty_string_input))
print('\n')

invalid_input = "20200230"
try:
    print("Invalid Input: {}".format(invalid_input))
    output_for_invalid_input = validation_parse_func(invalid_input)
except Exception as e:
    print("Raised Exception: {}".format(str(e)))
finally:
    print('\n')

invalid_input = datetime.datetime.strptime("20201001", "%Y%m%d")
try:
    print("Invalid Input: {}".format(invalid_input))
    output_for_invalid_input = validation_parse_func(invalid_input)
except Exception as e:
    print("Raised Exception: {}".format(str(e)))
finally:
    print('#' * 125)
