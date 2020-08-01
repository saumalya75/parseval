# `parseval`: A pythonic data validator 
**_parseval_** is a data validation tool for python. It provides numerous API to parse and validate data for all native data-types. it handles data on atomic level and focuses on validation part primarily.
<pre>
</pre>
Currently `parseval` supports following data types:  
* String  
* Integer  
* Numeric/Float  
* Date  
* DateTime  
<pre>
</pre>
The library will be updated in future to support more native data types and some complex types. Users can also create their own parser class just by inheritin gthe `FieldParser` class, but they have to follow build design pattern, like it is done in the existing parsers.  
<pre>




</pre>
## Who will be benefited?  
The philosophy behind making the repository available to community is to help everyone tackle a very un-rewarding (extremely messy at times) task of validating raw input data.  
<pre>
</pre>
So any user who works with raw source data and wants to be absolutely sure about the data she/he is getting before moving forward, will be benefited from this library. Here are some use cases:  
* ETL process (keep in mind data read is not part of the library)  
* Data scraping and machine learning data collection  
* Data quality assurance (maximum, minimum allowed value, Null check, custom check)  
* Validating data from any ORM/CRM systems etc.  
<pre>




</pre>
  
## What to expect?  
`parseval` is built to **validate one value at a time**(not an entire file at a single go), which gives the user extreme flexibility. Theoretically, user can validate any data (structured, semi structured and unstructured) using the library.  
<pre>
</pre>
As an add-on feature this library also has a built in `Parser` class which can handle following data collections  _TextIO()_, _list of json_ and _list of rows_, we will discuss about the usage in detail in later sections.  
<pre>
</pre>
The library is also capable of validating _slice of data_, which makes it absolutely trivial to parse `fixed-width` rows. One `regex pattern check` API also comes as built-in feature.  
<pre>




</pre>
## How to use?  
Now the fun part. We will first check the available features. Then we will go through the actual parsing & validation of atomic data. We will also see how the built in `parser` API can parse and validate entire data-collection.  
<pre>

</pre>
### Features
Current version comes with following six types of parsers:  
- `FieldParser` - _the parser to handle data which has no strict type specification_  
- `StringParser` - _the parser to handle `String` type data_  
- `FloatParser` - _the parser to handle `Numeric`/`Float` type data_  
- `IntegerParser` - _the parser to handle `Integer` type data_  
- `DatetimeParser` - _the parser to handle `Date` and `Timestamp` type data_  
- `ConstantParser` - _the parser which always returns a specified constant value, mostly used in data-collection parsing_
<pre>
</pre>
Each of these parsers comes with some common validations. Some parsers come with specific validations also. Following are all available validations.  
|             | **FieldParser**    | **StringParser**   | **FloatParser**    | **IntegerParser**  | **DatetimeParser** | **ConstantParser** | **Remarks**                                                                     |
|-------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|---------------------------------------------------------------------------------|
| not_null    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | Checks if the input data is not null                                            |
| value_set   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | Checks if input data matches with any of the values of a provided list of value |
| max_value   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | Checks if input data is less than or equals to Maximum allowed value            |
| min_value   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | Checks if input data is higher than or equals to Minimum allowed value          |
| range       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | Checks if input data reside in Allowed range of values                          |
| regex_match | :x:                | :heavy_check_mark: | :x:                | :x:                | :x:                | :x:                | Checks if input data matches with provided pattern                              |
| change_case | :x:                | :heavy_check_mark: | :x:                | :x:                | :x:                | :x:                | Returns data with altered case, _Not a validator_                               |
| convert     | :x:                | :x:                | :x:                | :x:                | :heavy_check_mark: | :x:                | Returns data in desired format, _Not a validator_                               |

Apart from these APIs user can use `add_function` API of any parser to add their custom validation/conversion function, given that the function always returns the same data or processed data. We will one example related to that also.
<pre>

</pre>
### Atomic value parsing  
<pre>
</pre>
**> Principle:** Now based on the data in hand, first choose a parser. Then apply the validation (`not_null`, `max_val` etc) as per requirements.
<pre>
</pre>
**> Scenario:** Built a parser for string input data that is not null and starts with 'DEMO_' string.
<pre>
</pre>
**> Solution:**
The process contains two trivial steps,  
1. Define the parser based on requirement  
2. Build the parser
3. Pass the value through the parser  
<pre>
</pre>
First let's build the parser,
```
>>> from parseval.parser import StringParser
>>> p_def = StringParser().not_null().regex_match(r'DEMO\_.*')
```
- `StringParser()` part will initialize the parser,
- `not_null()`, `regex_match()` are validators
<pre>
</pre>
Then we will build the parser:
```
>>> p_func = p_def.build()
```
- `build()` API needs to be applied on each the to build the validation functions to be applied on the data.
<pre>
</pre>
Now we will pass the input to the parser to get validated/parsed/converted data,
```
>>> input_data = "DEMO_DATA"
>>> ret = p_func(input_data)
>>> print(ret)
DEMO_DATA
```
<pre>

</pre>
**> Special features**,
> **Adding custom validation**
Let's say user want's to check whether the input number is even or odd, if the number is odd then return **0**. First we define the function encapsulating the logic:
>> \>>> def odd_even_handler(data: int):
>>
>>\>>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return data if data % 2 == 0 else 0
>
>Then add this function to parser object:
>> \>>> from parseval.parser import IntegerParser
>>
>> \>>> p_def = IntegerParser().not_null()**.add_func(odd_even_handler)**
>>
>> \>>> p_func = p_def.build()
>>
>>  \>>> print(p_func(13))
>>
>> 0
>>
>> \>>> print(p_func(12))
>>
>> 12
>
>**_Note: Accept only one argument(input data) in the custom function and remember to return validated/parsed/converted data._**
<pre>


</pre>
### Parsing data collections (TextIO, List of rows or json)
<pre>
</pre>
**> Principle:** Create an object of `parseval.Parser` class by providing expected structure of the data (we call it a schema) and call `parser` method of that object and pass the schema and data collection to get the parsed valid rows in return.
<pre>
</pre>
**> Scenario:** Parse the data of a file containing 3 columns.
<pre>
</pre>
**> Solution:**
The process contains three simple steps,  
1. Define a schema of parsers
2. Create `Parser` object by passing the `schema`. There is a way to set error threshold using `stop_on_error` parameter while creating the object. Please check API documents. Moreover `row delimiter` must be provided at this stage only for delimited files. 
3. Call `parse` method of that object and pass the data collection.
<pre>
</pre>
First let's built the schema, schema structure must be `list of tuples`, tuples will hold the `column name` as first element and the parser definition as second element. The sequence of list should match the column list in a record. We will create one file to use as a source file also:
```
>>> from parseval.parser import StringParser, IntegerParser,DatetimeParser, Parser
>>> with open('some_file.txt', 'w') as sf:
>>>		sf.writelines('1|MAEVE WILEY|19911024')
>>>		sf.writelines('2|OTIS MILLBURN|19920314')
>>> schema = [
	('id`, IntegerParser().not_null()),
	('name`, StringParser().not_null().regex_match(r'DEMO\_.*')),
	('dob`, DatetimeParser(formats='%Y%m%d').convert('%Y/%m/%d'))
]
```
Now, we will create an object of `Parser` class. Notice, apart from `schema` we are providing some more parameters, to know the functionality of those parameters in depth, please visit the library documentation.
```
>>> parser_obj = Parser(schema=schema,
		input_row_format = "delimited",
		parsed_row_format = "json",
		input_row_sep = "|",
		stop_on_error=0
	)
```
Now that we have the schema and the parsed object, we can parse the data:
```
>>> with open('some_file.txt', 'r') as sf:
>>> 	parsed_data = parser_obj.parse(sf)
>>> for l in parsed_data:
>>> 	print(l)
{'id': 1, 'name': 'MAEVE WILEY', 'dob': '1991/10/24'}
{'id': 2, 'name': 'OTIS MILLBURN', 'dob': '1992/03/14'}
```
<pre>

</pre>
**> Special features**,
> **Parsing Fixed-Width dataset**
If the source data rows are not delimited like previous case, instead it is fixed width, then use `start` and `end` parameter provided in each parser to mention start and end position for each column while creating the schema, and mention `input_row_format` as **`fixed-width`**. Note `input_row_sep` parameter has no effect in this scenario. Rest of the processes are same. Please checkout following code snippet which handled the act same data in fixed-width format.
```
>>> from parseval.parser import StringParser, IntegerParser,DatetimeParser, Parser
>>> with open('some_file.txt', 'w') as sf:
>>>		sf.writelines('1MAEVE WILEY  19911024')
>>>		sf.writelines('2OTIS MILLBURN19920314')
>>> schema = [
	('id`, IntegerParser(start=1, end=1).not_null()),
	('name`, StringParser(start=2, end=14).not_null().regex_match(r'DEMO\_.*')),
	('dob`, DatetimeParser(start=15, end=22, formats='%Y%m%d').convert('%Y/%m/%d'))
]
>>> parser_obj = Parser(schema=schema,
		input_row_format = "delimited",
		parsed_row_format = "json",
		input_row_sep = "|",
		stop_on_error=0
	)
>>> with open('some_file.txt', 'r') as sf:
>>> 	parsed_data = parser_obj.parse(sf)
>>> for l in parsed_data:
>>> 	print(l)
{'id': 1, 'name': 'MAEVE WILEY', 'dob': '1991/10/24'}
{'id': 2, 'name': 'OTIS MILLBURN', 'dob': '1992/03/14'}
```
**_Note: `start` and `end` are position of the characters(starting with 1, not 0) in the row. Moreover, both positions are included while slicing._**
<pre>




</pre>
---
---
_**That's all from my end. Hope you find the library useful in your daily data engineering. Please reach out for any queries or suggestion. Feel free to use and enrich the code. I am avaiable at saumalya75@gmail.com  and [linkedin.com/in/saumalya-sarkar-b3712817b](https://www.linkedin.com/in/saumalya-sarkar-b3712817b) .**_