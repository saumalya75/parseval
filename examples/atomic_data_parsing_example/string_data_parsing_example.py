# Import required parser class
from parseval.parser import StringParser

basic_parser = StringParser()  # Create basic parser object
basic_parse_func = basic_parser.build()  # Build the parser function
input_data = 'Any String'  # Input Data
basic_parsed_output = basic_parse_func(input_data)  # Parse data

print('#' * 50, " STRING PARSING ", '#' * 50)
print('====>', "Simple Data Parsing example:")
print("Input 1: {}".format(input_data))
print("Output 1: {}".format(basic_parsed_output))
print('\n')


# Now let's see some available validators, to get the idea of how to use those
# Note, we will not go through all available validators, because all validators work in same fashion
# Syntax and description of all validators are available in documentation

validation_parser = StringParser()\
    .not_null(default_value="NA")\
    .value_set(["Apple", "Google", "NA"])  # null check validation and allowed values validation is added
validation_parse_func = validation_parser()  # Yes, you can directly call the object to build the parser

valid_input_data = 'Apple'
output_for_valid_input_data = validation_parse_func(valid_input_data)  # Parse data
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

invalid_input = "Microsoft"
try:
    print("Invalid Input: {}".format(invalid_input))
    output_for_invalid_input = validation_parse_func(invalid_input)
except Exception as e:
    print("Raised Exception: {}".format(str(e)))
finally:
    print('#' * 125)
