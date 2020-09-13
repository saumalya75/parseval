import logging
from parseval.parser import StringParser
# Special Feature 1: Add custom validation
# This feature is available on all the parsers, the example will be shown on StringParser

logging.basicConfig(format='%(levelname)s:%(asctime)s:: %(message)s', level=logging.DEBUG)


# Adding custom validation that the first 3 digit is from a set of values
def _first_three_char_check(data: str):
    list_of_allowed_value: list = ['ABC', 'DEF']
    if not data:
        return data

    if str(data)[:3].upper() in [word.upper() for word in list_of_allowed_value]:
        return data
    else:
        raise Exception("Bad prefix in the value.")


# Create and build the parser
parser = StringParser().add_func(_first_three_char_check)
parser_func = parser.build()

input_data = "ABC2344"
logging.info(('#' * 50) + " ADDING CUSTOM VALIDATOR " + ('#' * 50))
logging.info("====> Valid Input:")
logging.info("Input: {}".format(input_data))
logging.info("Output: {}".format(parser_func(input_data)))
logging.info('\n')

input_data = "PQR12344"
logging.info("====> Invalid Input:")
try:
    logging.info("Invalid Input: {}".format(input_data))
    parser_func(input_data)
except Exception as e:
    logging.error("Raised Exception: {}".format(str(e)))
finally:
    logging.info("\n\n")


# Special Feature 2: Data Slicing
# All the parsers come with built-in slicing features, mainly built to support fixed width rows
# Please note, while using slicing, rest of the data will be scraped
# Provide actual character position, index starting from 1, lower-bound and upper-bound both inclusive
slicing_parser = StringParser(start=1, end=3).value_set(['ABC', 'DEF'])
slicing_parser_func = slicing_parser.build()

input_data = "ABC|2344"
logging.info(('#' * 50) + " SLICING DATA " + ('#' * 50))
logging.info("====> Valid Input:")
logging.info("Input: {}".format(input_data))
logging.info("Output: {}".format(slicing_parser_func(input_data)))
logging.info('\n')

input_data = "PQR|2344"
logging.info("====> Invalid Input:")
try:
    logging.info("Invalid Input: {}".format(input_data))
    slicing_parser_func(input_data)
except Exception as e:
    logging.error("Raised Exception: {}".format(str(e)))
finally:
    logging.info("\n\n")


# Special Feature 3: Parser Creation Syntactic Sugar
# This one is less of a feature, moreof a syntactic sugar, for users.
# As already established, steps of usage are:
#   1. Create a parser object,
#   2. Call validator methods of the object,
#   3. Call `build` method of the object to generate actual parser method
# Instead of doing the third step, user can directly call the object to get the parser function.
# Note, only the validators that are called prior to the call will be applied.
parser = StringParser().not_null()
parser_func = parser()  # Instead of using `build()` we directly called the parser object

input_data = "ABC|2344"
logging.info(('#' * 50) + " SYNTACTIC SUGAR " + ('#' * 50))
logging.info("====> Valid Input:")
logging.info("Input: {}".format(input_data))
logging.info("Output: {}".format(parser_func(input_data)))
logging.info('#' * 125)
