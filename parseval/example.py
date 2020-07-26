try:
    from parseval.parser import *
except ImportError:
    from parser import *

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
         .not_null(0)
         ),
        ('C7', ConstantParser('Iron-Man'))
    ]
    p = Parser(schema=schema)
    parsed_data = p.parse([
        '""|Trig_2020-23-12|A|20200123|2000|21.0934|',
        '"DEF"||abc||||',
        '"DEF"|Manual_2020-23-12||2020-01-23 10:20:23|1200|11|'
    ])
    print(parsed_data)


    """
    Example with Fixed-width data
    """
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
    print(parsed_data)

