# `parseval`: A pythonic data validator 
**_parseval_** is a data validation tool for python. Following are the available parsers:

## FieldParser:

**Signature**: _FieldParser(start: int = 0, end: int = 0, quoted: int = 0)_

**Parameters**:

- `start`: Start position of the data in row

- `end`: End position of the data in row

- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value: any = None)_
>
> **Parameters**:
>
> - `default_value`: Default value for a column which should be not null
>
<pre>
</pre>
>
> **Signature**: _value_set(values: typing.List, nullable: bool = True)_
>
> **Parameters**:
>
> - `values`: Set of valid values for this column
> - `nullable`: If set to `True` then `empty string` and `None` will be treated as valid value, along with the provided value list
>
<pre>
</pre>
>
> **Signature**: _max_value(value: any)_
>
> **Parameters**:
>
> - `values`: Maximum allowed value for the column
>
<pre>
</pre>
>
> **Signature**: _min_value(value: any)_
>
> **Parameters**:
>
> - `values`: Minimum allowed value for the column
>
<pre>
</pre>
>
> **Signature**: _range(lower_bound: any, upper_bound: any)_
>
> **Parameters**:
>
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column
>
<pre>
</pre>
---
## StringParser:

**Signature**: _StringParser(start: int = 0, end: int = 0, quoted: int = 0)_

**Parameters**:

- `start`: Start position for the column in the row

- `end`: End position for the column in the row

- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value: str = None, allow_white_space: bool = False)_
>
> **Parameters**:
>
>- `default_value`: Default value for a column which should be not null
>- `allow_white_space`: If set to `True`, whitespaces will not be treated as `Null` value.
>
<pre>
</pre>
> **Signature**: _value_set(values: typing.List[str], nullable: bool = True)_
>
> **Parameters**:
>
> - `values`: Set of valid values for this column
> - `nullable`: If set to `True` then empty string and None will be treated as valid value, along with the provided value list
>
<pre>
</pre>
> **Signature**: _max_value(value: str)_
>
> **Parameters**:
>
> - `values`: Maximum allowed value for the column
>
<pre>
</pre>
> **Signature**: _min_value(value: str)_
>
> **Parameters**:
>
> - `values`: Minimum allowed value for the column
>
<pre>
</pre>
> **Signature**: _regex_match(pattern: str, nullable=True)_
>
> **Parameters**:
>
> - `pattern`: Patter to match with the data
> - `nullable`: If set to `True` then empty string and None will be treated as valid value, along with the values that matches provided `pattern`
>
<pre>
</pre>
> **Signature**: _change_case(case_type: str = 'S')_
>
> **Parameters**:
>
> - `case_type`: Target case: {'U'/'u': UPPERCASE, 'L'/'l': lowercase, 'S'/'s': Sentence Case}
>
<pre>
</pre>
> **Signature**: _range(lower_bound: str, upper_bound: str)_
>
> **Parameters**:
>
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column
>
<pre>
</pre>
---
## FloatParser:

**Signature**: _FloatParser(start: int = 0, end: int = 0, quoted: int = 0)_

**Parameters**:

- `start`: Start position for the column in the row

- `end`: End position for the column in the row

- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value: float = None)_
>
> **Parameters**:
>
>- `default_value`: Default value for a column which should be not null
>
<pre>
</pre>
> **Signature**: _value_set(values: typing.List[float], nullable: bool = True)_
>
> **Parameters**:
>
> - `values`: Set of valid values for this column
> - `nullable`: If set to `True` then empty string and None will be treated as valid value, along with the provided value list
>
<pre>
</pre>
> **Signature**: _max_value(value: float)_
>
> **Parameters**:
>
> - `values`: Maximum allowed value for the column
>
<pre>
</pre>
> **Signature**: _min_value(value: float)_
>
> **Parameters**:
>
> - `values`: Minimum allowed value for the column
>
<pre>
</pre>
> **Signature**: _range(lower_bound: float, upper_bound: float)_
>
> **Parameters**:
>
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column
>
---
## IntegerParser:

**Signature**: _IntegerParser(start: int = 0, end: int = 0, quoted: int = 0)_

**Parameters**:

- `start`: Start position for the column in the row

- `end`: End position for the column in the row

- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value: int = None)_
>
> **Parameters**:
>
>- `default_value`: Default value for a column which should be not null
>
<pre>
</pre>
> **Signature**: _value_set(values: typing.List[int], nullable: bool = True)_
>
> **Parameters**:
>
> - `values`: Set of valid values for this column
> - `nullable`: If set to `True` then empty string and None will be treated as valid value, along with the provided value list
>
<pre>
</pre>
> **Signature**: _max_value(value: int)_
>
> **Parameters**:
>
> - `values`: Maximum allowed value for the column
>
<pre>
</pre>
> **Signature**: _min_value(value: int)_
>
> **Parameters**:
>
> - `values`: Minimum allowed value for the column
>
<pre>
</pre>
> **Signature**: _range(lower_bound: int, upper_bound: int)_
>
> **Parameters**:
>
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column
>
<pre>
</pre>
---
## DatetimeParser:

**Signature**: _DatetimeParser(start: int = 0, end: int = 0, formats: typing.List =['%Y%m%d', '%Y%md%H%M%S'], quoted: int = 0)_

**Parameters**:

- `start`: Start position for the column in the row

- `end`: End position for the column in the row

- `formats`: Format of date/datetime used in the input data

- `quoted`: Data quotation options - {0: Not Quoted, 1: Double Quoted, 2: Single Quoted}

Available APIs:

> **Signature**: _not_null(default_value: typing.Union[str, datetime.datetime] = None, format: str = '%Y-%m-%d %H:%M:%S')_
>
> **Parameters**:
>
> - `default_value`: Default value for a column which should be not null
> - `format`: Provided default value format, if a datetime object is provided as default value, then this parameter has no effect.
>
<pre>
</pre>
> **Signature**: _value_set(values: typing.List[typing.Union[str, datetime.datetime]], format='%Y-%m-%d %H:%M:%S', nullable: bool = True)_
>
> **Parameters**:
>
> - `values`: Set of valid values for this column
> - `format`: Provided allowed value's format, if a datetime object is provided as allowed value, then this parameter has no effect.
> - `nullable`: If set to `True` then empty string and None will be treated as valid value, along with the provided value list
>
<pre>
</pre>
> **Signature**: _max_value(value: typing.Union[str, datetime.datetime], format: str = '%Y-%m-%d %H:%M:%S')_
>
> **Parameters**:
>
> - `values`: Maximum allowed value for the column
> - `format`: Provided allowed value's format, if a datetime object is provided as allowed value, then this parameter has no effect.
>
<pre>
</pre>
> **Signature**: _min_value(value: typing.Union[str, datetime.datetime], format: str = '%Y-%m-%d %H:%M:%S')_
>
> **Parameters**:
>
> - `values`: Minimum allowed value for the column
> - `format`: Provided allowed value's format, if a datetime object is provided as allowed value, then this parameter has no effect.
>
<pre>
</pre>
> **Signature**: _range(lower_bound: typing.Union[str, datetime.datetime], upper_bound: typing.Union[str, datetime.datetime], format='%Y-%m-%d %H:%M:%S')_
>
> **Parameters**:
>
> - `lower_bound`: Minimum allowed value for the column
> - `upper_bound`: Maximum allowed value for the column
> - `format`: Provided allowed value's format, if a datetime object is provided as allowed value, then this parameter has no effect.
>
---
## ConstantParser:

**Signature**: _ConstantParser(value)_

**Parameters**:

- `value`: The parser will always return this value irrespective of the input data and called methods.

---
<pre>



</pre>

_For any further queries reach out to **saumalya75@gmail.com** or **http://linkedin.com/in/saumalya-sarkar-b3712817b**_

---
