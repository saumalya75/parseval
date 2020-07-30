import tempfile
try:
    from parseval.parser import *
except ImportError:
    from parser import *


def parity_check(data):
    if data:
        try:
            i_Data = int(data)
        except:
            pass
        if i_Data % 2 != 0:
            raise Exception("The data has to be even!")
    return data


if __name__ == "__main__":
    """
    Example with delimited data
    """
    schema = [
        ('C1', FieldParser(quoted=1)),
        ('C2', StringParser()
         .regex_match(r'\w+_\d{4}-\d{2}-\d{2}')
         .change_case('u')
         ),
        ('C3', FieldParser(start=1, end=1)
         .value_set(['a', 'b', 'A'])
         ),
        ('C4', DatetimeParser(formats=['%Y%m%d', '%Y-%m-%d %H:%M:%S'])
         .convert('%Y/%m/%d')
         .max_value(datetime.datetime.now())
         .min_value(value='20000101', format='%Y%m%d')
         .not_null(datetime.datetime.strptime('19001231', '%Y%m%d'))
         ),
        ('C5', IntegerParser()
         .max_value(2000)
         .not_null(default_value=0)
         ),
        ('C6', FloatParser()
         .min_value(10.0)
         .not_null(0.0)
         ),
        ('C7', ConstantParser('Iron-Man')),
        ('C8', IntegerParser().add_func(parity_check).range(0, 40))
    ]
    p = Parser(schema=schema, stop_on_error=-1)

    """
        Input structure: List of rows
    """
    parsed_data = p.parse([
        '""|Trig_202-23-12|A|20200123|2000|21.0934||10',
        '"DEF"||abc|||||34',
        '"DEF"|Manual2020-23-12||2020-01-23 10:20:23|1200|11||'
    ])
    for line in parsed_data:
        print(line)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
          " LIST OF LINES ARE PARSED "
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    """
        Input structure: File object
    """
    p = Parser(schema=schema, stop_on_error=1)
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as sf:
            sf.writelines('""|Trig2020-23-12|A|20200123|2000|21.0934||10\n')
            sf.writelines('"DEF"||abc|||||34\n')
            sf.writelines('"DEF"|Manual_2020-23-12||2020-01-23 10:20:23|1200|11||')

        with open(tf.name, 'r') as sf:
            for line in p.parse(sf):
                print(line)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
          " FILE DATA IS PARSED "
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    """
    Example with Fixed-width data
    """
    p = Parser(schema=schema, stop_on_error=0)
    fw_schema = [
        ('C1', FieldParser(1, 2)),
        ('C2', StringParser(3, 5).change_case('U').not_null('nan', allow_white_space=True)),
        ('C3', FieldParser(6, 6).value_set(['M', 'F'])),
        ('C4', FieldParser(7, 11).not_null('dummy')),
        ('C5', FieldParser(7, 11)),
        ('C6', IntegerParser(12, 13).max_value(20)),
        ('C7', FloatParser(14, 17).min_value(10.0))
    ]
    p = Parser(schema=fw_schema, input_row_format='fixed-width', parsed_row_format='json')
    parsed_data = p.parse([
        'd0sauMvalue191000',
        'd0pouM     2090.03'
    ])
    for line in parsed_data:
        print(line)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
          " FIXED-WIDTH LINES ARE PARSED "
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

