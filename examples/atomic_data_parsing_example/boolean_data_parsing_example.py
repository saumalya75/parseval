# Import required parser class
import logging
from parseval.parser import BooleanParser

logging.basicConfig(format='%(levelname)s:%(asctime)s:: %(message)s', level=logging.DEBUG)
basic_parser = BooleanParser()  # Create basic parser object
basic_parse_func = basic_parser.build()  # Build the parser function
input_data = 'True'  # Input Data
basic_parsed_output = basic_parse_func(input_data)  # Parse data

logging.info(('#' * 50) + " BOOLEAN PARSING " + ('#' * 50))
logging.info("====> Simple Data Parsing example:")
logging.info("Output 1: {}".format(basic_parsed_output))
logging.info("Type of Output 1: {}".format(type(basic_parsed_output)))
logging.info('\n\n')


# As expected data type of input data is converted to Boolean, to prevent that
# we will set `enforce_type` parameter to `False` while creating the parser object


non_type_enforcing_parser = BooleanParser(enforce_type=False)  # Create new parser object
non_type_enforcing_parse_func = non_type_enforcing_parser.build()  # Build new parser function
non_type_enforcing_parsed_output = non_type_enforcing_parse_func(input_data)  # parse same data

logging.info("====> Data Parsing without enforcing type conversion example:")
logging.info("Output 2: {}".format(non_type_enforcing_parsed_output))
logging.info("Type of Output 2: {}".format(type(non_type_enforcing_parsed_output)))
logging.info('\n\n')

# Let's try some other types of data to show which values are parsed to True and which are to False:
list_of_input_data = ['True', 'fAlSe', 'T', 'F', 'Y', 'N', 'yES',
                      'No', 1, 1.9, -2, 0, 0.0, True, False
                      ]  # List of input data
logging.info("====> Parsing multiple types of data:")
for input_data in list_of_input_data:
    logging.info("Input: {} >>> Output: {}.".format(input_data, basic_parse_func(input_data)))
logging.info('#' * 125)
