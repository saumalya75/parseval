# `parseval`: A pythonic data validator 
**_parseval_** is a data validation tool for python. Following are the available parsers:

## FieldParser:
**Signature**: _FieldParser(start=0, end=0, quoted=0)_

**Parameters**:
- `start`: Start position of the data in row
- `end`: End position of the data in row
- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value=None)_
>
> **Parameters**:
> * `default_value`: Default value for a column which should be not null
<pre>
</pre>
> **Signature**: _value_set(values, nullable=True)_
>
> **Parameters**:
> - `values`: Set of valid values for this column
> - `nullable`: If set to `True` then `empty string` and `None` will be treated as valid value, along with the provided value list


> **Signature**: _max_value(value)_
>
> **Parameters**:
> - `values`: Maximum allowed value for the column


> **Signature**: _min_value(value)_
>
> **Parameters**:
> - `values`: Minimum allowed value for the column


> **Signature**: _range(lower_bound, upper_bound)_
>
> **Parameters**:
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column

---
## StringParser:
**Signature**: _StringParser(start=0, end=0, quoted=0)_

**Parameters**:
- `start`: Start position for the column in the row
- `end`: End position for the column in the row
- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value=None, allow_white_space=False)_
>
> **Parameters**:
>- `default_value`: Default value for a column which should be not null
>- `allow_white_space`: If set to `True`, whitespaces will not be treated as `Null` value.


> **Signature**: _value_set(values, nullable=True)_
>
> **Parameters**:
> - `values`: Set of valid values for this column
> - `nullable`: If set to `True` then empty string and None will be treated as valid value,
             along with the provided value list

> **Signature**: _max_value(value)_
>
> **Parameters**:
> - `values`: Maximum allowed value for the column


> **Signature**: _min_value(value)_
>
> **Parameters**:
> - `values`: Minimum allowed value for the column


> **Signature**: _regex_match(pattern, nullable=True)_
>
> **Parameters**:
> - `pattern`: Patter to match with the data
> - `nullable`: If set to `True` then empty string and None will be treated as valid value,
             along with the values that matches provided `pattern`


> **Signature**: _change_case(case_type='S')_
>
> **Parameters**:
> - `case_type`: Target case: {'U'/'u': UPPERCASE, 'L'/'l': lowercase, 'S'/'s': Sentence Case}


> **Signature**: _range(lower_bound, upper_bound)_
>
> **Parameters**:
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column

---
## FloatParser:
**Signature**: _FloatParser(start=0, end=0, quoted=0)_

**Parameters**:
- `start`: Start position for the column in the row
- `end`: End position for the column in the row
- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value=None)_
>
> **Parameters**:
>- `default_value`: Default value for a column which should be not null


> **Signature**: _value_set(values, nullable=True)_
>
> **Parameters**:
> - `values`: Set of valid values for this column
> - `nullable`: If set to `True` then empty string and None will be treated as valid value,
             along with the provided value list

> **Signature**: _max_value(value)_
>
> **Parameters**:
> - `values`: Maximum allowed value for the column


> **Signature**: _min_value(value)_
>
> **Parameters**:
> - `values`: Minimum allowed value for the column


> **Signature**: _range(lower_bound, upper_bound)_
>
> **Parameters**:
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column

---
## IntegerParser:
**Signature**: _IntegerParser(start=0, end=0, quoted=0)_

**Parameters**:
- `start`: Start position for the column in the row
- `end`: End position for the column in the row
- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value=None)_
>
> **Parameters**:
>- `default_value`: Default value for a column which should be not null


> **Signature**: _value_set(values, nullable=True)_
>
> **Parameters**:
> - `values`: Set of valid values for this column
> - `nullable`: If set to `True` then empty string and None will be treated as valid value,
             along with the provided value list

> **Signature**: _max_value(value)_
>
> **Parameters**:
> - `values`: Maximum allowed value for the column


> **Signature**: _min_value(value)_
>
> **Parameters**:
> - `values`: Minimum allowed value for the column


> **Signature**: _range(lower_bound, upper_bound)_
>
> **Parameters**:
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column

---
## DatetimeParser:
**Signature**: _DatetimeParser(start=0, end=0, formats=['%Y%m%d', '%Y%md%H%M%S'])_

**Parameters**:
- `start`: Start position for the column in the row
- `end`: End position for the column in the row
- `formats`: Format of date/datetime used in the input data
- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value=None, format='%Y-%m-%d %H:%M:%S')_
>
> **Parameters**:
> - `default_value`: Default value for a column which should be not null
> - `format`: Provided default value format, if a datetime object is provided as default value, then this parameter has no effect.


> **Signature**: _value_set(values, format='%Y-%m-%d %H:%M:%S', nullable=True)_
>
> **Parameters**:
> - `values`: Set of valid values for this column
> - `format`: Provided allowed value's format, if a datetime object is provided as allowed value, then this parameter has no effect.
> - `nullable`: If set to `True` then empty string and None will be treated as valid value,
             along with the provided value list

> **Signature**: _max_value(value, format='%Y-%m-%d %H:%M:%S')_
>
> **Parameters**:
> - `values`: Maximum allowed value for the column
> - `format`: Provided allowed value's format, if a datetime object is provided as allowed value, then this parameter has no effect.


> **Signature**: _min_value(value, format='%Y-%m-%d %H:%M:%S')_
>
> **Parameters**:
> - `values`: Minimum allowed value for the column
> - `format`: Provided allowed value's format, if a datetime object is provided as allowed value, then this parameter has no effect.


> **Signature**: _range(lower_bound, upper_bound, format='%Y-%m-%d %H:%M:%S')_
>
> **Parameters**:
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column
> - `format`: Provided allowed value's format, if a datetime object is provided as allowed value, then this parameter has no effect.
## ConstantParser:
**Signature**: _ConstantParser(value)_

**Parameters**:
- `value`: The parser will always return this value irrespective of the input data and called methods.
---
<pre>



</pre>
_**That's all from my end. Hope you find the library useful in your daily data engineering. Please reach out for any queries or suggestion. Feel free to use and enrich the code. I am always avaiable at saumalya75@gmail.com **_
