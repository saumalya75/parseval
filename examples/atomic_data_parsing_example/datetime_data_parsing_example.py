# Import required parser class
from parseval.parser import DatetimeParser
import datetime
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s:: %(message)s', level=logging.DEBUG)
basic_parser = DatetimeParser(formats=['%Y%m%d'])  # Create basic parser object
basic_parse_func = basic_parser.build()  # Build the parser function
input_data = "20200101"  # Input Data
basic_parsed_output = basic_parse_func(input_data)  # Parse data

logging.info(('#' * 50) + " DATETIME PARSING " + ('#' * 50))
logging.info("====> Simple Data Parsing example:")
logging.info("Input 1: {}".format(input_data))
logging.info("Output 1: {}".format(basic_parsed_output))
logging.info('\n')


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
logging.info("====> Data Validation example:")
logging.info("Input 2: {}".format(valid_input_data))
logging.info("Output 2: {}".format(output_for_valid_input_data))
logging.info('\n')

null_input = None
output_for_null_input = validation_parse_func(null_input)
logging.info("Input 3: {}".format(null_input))
logging.info("Output 3: {}".format(output_for_null_input))
logging.info('\n')

empty_string_input = ""
output_for_empty_string_input = validation_parse_func(empty_string_input)
logging.info("Input 4: {}".format(empty_string_input))
logging.info("Output 4: {}".format(output_for_empty_string_input))
logging.info('\n')

invalid_input = "20200230"
try:
    logging.info("Invalid Input: {}".format(invalid_input))
    output_for_invalid_input = validation_parse_func(invalid_input)
except Exception as e:
    logging.error("Raised Exception: {}".format(str(e)))
finally:
    logging.info('\n')

invalid_input = datetime.datetime.strptime("20201001", "%Y%m%d")
try:
    logging.info("Invalid Input: {}".format(invalid_input))
    output_for_invalid_input = validation_parse_func(invalid_input)
except Exception as e:
    logging.error("Raised Exception: {}".format(str(e)))
finally:
    logging.info('#' * 125)
