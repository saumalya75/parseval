
# `parseval`: A pythonic data validator 

**_parseval_** is a data validation tool for python. It provides numerous API to parse and validate data for all native data-types. it handles data on atomic level and focuses on validation part primarily.  
<pre>  
</pre>  
Currently `parseval` supports following data types:    
* String    
* Integer /Long  
* Numeric/Float    
* Boolean
* Date    
* DateTime    
<pre>  
</pre>  
The library will be updated in future to support more native data types and some complex types. Users can also create their own parser class just by inheriting the `FieldParser` class, but they have to follow build design pattern, like it is done in the existing parsers.    
<pre>  
</pre>  
>**API reference:**  [https://parseval.readthedocs.io/en/latest/](https://parseval.readthedocs.io/en/latest/)  
<pre>  
  
  
  
  
</pre>  
## Who will be benefited?   
Any user who handle raw source data and wants to be absolutely sure about the data format.  
  
Here are some use cases:    
* ETL process (keep in mind data read is not part of the library)    
* Data scraping and machine learning data collection    
* Data quality assurance (maximum, minimum allowed value, Null check, custom check)    
* Validating data from any ORM/CRM systems etc.    
<pre>  
  
  
  
  
</pre>  
    
## What to expect? 

`parseval` is built to **validate one value at a time**(not an entire file at a single go), which gives the user extreme flexibility. Theoretically, user can validate any data (structured, semi structured and unstructured) using the library.    
  
  
As an add-on feature this library also has a built in `Parser` class which can handle following data collections  _**TextIO**_, _**list of json**_ and _**list of rows**_, we will discuss about the usage in detail in later sections.    
  
  
The library is also capable of validating _slice of data_, which makes it absolutely trivial to parse `fixed-width` rows. One `regex pattern check` API also comes as built-in feature.    
<pre>  
  
  
  
  
</pre>  
## How to use?

Now the fun part. We will first check the available features. Then we will go through the actual parsing & validation of atomic data. We will also see how the built in `parser` API can parse and validate entire data-collection. Example modules that are available in the repository are highly recommended.  
  
<pre>  
  
</pre>  
### Features  
Current version comes with following six types of parsers:    
- `FieldParser` - _the parser to handle data which has no strict type specification_
- `StringParser` - _the parser to handle `String` type data_ 
- `FloatParser` - _the parser to handle `Numeric`/`Float` type data_
- `IntegerParser` - _the parser to handle `Integer` type data_ 
- `BooleanParser` - _the parser to handle `Boolean` type data_ 
- `DatetimeParser` - _the parser to handle `Date` and `Timestamp` type data_ 
- `ConstantParser` - _the parser which always returns a specified constant value, mostly used in data-collection parsing_  
  
Each of these parsers comes with some common validations. Some parsers come with specific validations also. Following are all available validations.    
|             | **FieldParser**    | **StringParser**   | **FloatParser**    | **IntegerParser**  | **BooleanParser** | **DatetimeParser** | **ConstantParser** | **Remarks**                                                                     |
|-------------|--------------------|--------------------|--------------------|--------------------|-------------------|--------------------|--------------------|---------------------------------------------------------------------------------|
| not_null    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:               | :heavy_check_mark: | :x:                | Checks if the input data is not null                                            |
| value_set   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:               | :heavy_check_mark: | :x:                | Checks if input data matches with any of the values of a provided list of value |
| max_value   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:               | :heavy_check_mark: | :x:                | Checks if input data is lower than or equal to Maximum allowed value            |
| min_value   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:               | :heavy_check_mark: | :x:                | Checks if input data is higher than or equals to Minimum allowed value          |
| range       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:               | :heavy_check_mark: | :x:                | Checks if input data reside in Allowed range of values                          |
| regex_match | :x:                | :heavy_check_mark: | :x:                | :x:                | :x:               | :x:                | :x:                | Checks if input data matches with provided pattern                              |
| change_case | :x:                | :heavy_check_mark: | :x:                | :x:                | :x:               | :x:                | :x:                | Returns data with altered case, _Not a validator_                               |
| convert     | :x:                | :x:                | :x:                | :x:                | :x:               | :heavy_check_mark: | :x:                | Returns data in desired format, _Not a validator_                               |
  
Apart from these APIs user can use `add_func` API of any parser to add their custom validation/conversion function, given that the function always returns the same data or processed data. We will see one example related to that also.  
<pre>  
  
</pre>  
### Atomic value parsing   
  
**> Principle:** Now based on the data in hand, first choose a parser. Then apply the validation (`not_null`, `max_val` etc) as per requirements.  
  
**> Scenario:** Built a parser for string input data that is not null and starts with 'DEMO_' string.  
  
**> Solution:**  
The process contains two trivial steps,    
1. Define the parser based on requirement    
2. Build the parser  
3. Pass the value through the parser    
  
First let's build the parser,  
```  
>>> from parseval.parser import StringParser  
>>> p_def = StringParser().not_null().regex_match(r'DEMO\_.*')  
```  
- `StringParser()` part will initialize the parser,  
- `not_null()`, `regex_match()` are validators  
  
Then we will build the parser:  
```  
>>> p_func = p_def.build()  # p_func = p_def()
```  
- `build()` API needs to be applied on each the to build the validation functions to be applied on the data. Or the parser object can be called directly, which will have same effect. 
  
Now we will pass the input to the parser to get validated/parsed/converted data,  
```  
>>> input_data = "DEMO_DATA"  
>>> ret = p_func(input_data)  
>>> print(ret)  
'DEMO_DATA'  
```  
<pre>  
  
</pre>  
**> Special features**,  
> **Controlling Output Type**  
All the parser's come with trivial tendency to convert the input data to the type of parser it is. Meaning `IntegerParser` will always try to convert the input data to `int` type and produce the output, which kind of makes sense. But talking out of experience, some time we just want to check whether the data is compatible to be integer, we might not want to change it right away. Hence all the parsers accept one parameter `enforce_type`, which can be set to `False` to achieve exactly that. But keep in mind `enforce_type` is by-default set to `True`, hence if user don't disable it explicitly, parsers will change the type of the data:  
>> \>>> from parseval.parser import IntegerParser  
>>  
>> \>>> input = '13' ## string data
>>  
>> \>>> p_def = IntegerParser().build() ## Building right away
>>
>>  \>>> print(p_func(input))  
>>  
>> 13 ----------> Data is converted to Integer type while parsing
>>  
>> \>>> p_def = IntegerParser(**enforce_type=False**).build()
>>  
>> \>>> print(p_func(input))  
>>  
>> '13' ----------> Data is still String type even after parsing
>  
>**_Note: By default the parsers change the type of data because it's trivial that an `IntegerParser` will return `Integer`._**  
<pre>  
  
  
</pre>  
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
>> \>>> p_func = p_def()  
>>  
>> \>>> odd_input = 13
>>  
>> \>>> even_input = 12
>>  
>>  \>>> print(p_func(odd_input))  
>>  
>> 0  
>>  
>> \>>> print(p_func(even_input))  
>>  
>> 12  
>  
>**_Note: Accept only one argument(input data) in the custom function and remember to return validated/parsed/converted data._**  
<pre>  
  
  
</pre>  
### Parsing data collections (TextIO, List of rows or json)  
  
**> Principle:** Create an object of `parseval.Parser` class by providing expected structure of the data (we call it a schema) and call `parser` method of that object and pass the schema and data collection to get the parsed valid rows in return.  
  
**> Scenario:** Parse the data of a file containing 3 columns.  
  
**> Solution:**  
The process contains three simple steps,    
1. Define a schema of parsers  
2. Create `Parser` object by passing the `schema`. There is a way to set error threshold using `stop_on_error` parameter while creating the object. Please check API documents. Moreover `row delimiter` must be provided at this stage only for delimited files.   
3. Call `parse` method of that object and pass the data collection.  
  
First let's built the schema, schema structure must be `list of tuples`, tuples will hold the `column name` as first element and the parser definition as second element. The sequence of list should match the column list in a record. We will create one file to use as a source file also:  
```  
>>> from parseval.parser import StringParser, IntegerParser,DatetimeParser
>>> from parseval.parser import Parser  
>>> with open('some_file.txt', 'w') as sf:  
>>>       sf.writelines('1|MAEVE WILEY|19911024')  
>>>       sf.writelines('2|OTIS MILLBURN|19920314')  
>>> schema = [('id', IntegerParser(enforce_type=False).not_null()), ('name', StringParser(enforce_type=False).not_null()), ('dob', DatetimeParser(formats=['%Y%m%d'], enforce_type=False).convert('%Y/%m/%d'))]
```  
Now, we will create an object of `Parser` class. Notice, apart from `schema` we are providing some more parameters, to know the functionality of those parameters in depth, please visit the API reference link mentioned above.  
```
>>> parser_obj = Parser(schema=schema,  
 input_row_format = "delimited", parsed_row_format = "dict", input_row_sep = "|", stop_on_error=0 )
 ```  
Now that we have the schema and the parsed object, we can parse the data:  
```  
>>> with open('some_file.txt', 'r') as sf:  
>>>    parsed_data = parser_obj.parse(sf)  
>>> for l in parsed_data:  
>>>    print(l)  
{'id': 1, 'name': 'MAEVE WILEY', 'dob': '1991/10/24'}  
{'id': 2, 'name': 'OTIS MILLBURN', 'dob': '1992/03/14'}  
```  
The library takes in any kind of iterator as input data wrapper, provided that the wrapper returns one row at a time while looping. The data wrappers can be anything like `File I/O Wrapper`, `List`, `Generator Object` etc etc.
<pre></pre>
The library accepts data in multiple formats also, which can be tweaked using `input_row_format` parameter while creating the `Parser` object. Supported formats are:
- `delimited`: Delimited Lines in String format (`input_row_sep` parameter can be used to specify the delimiter, by0default it is `|`)
- `fixed-width`: Fixed-width Lines in String format
- `json`: Python `dictionary` object or `Json` data
<pre></pre>
Naturally the library supports multiple output data formats also, but keep in mind it will always return an generator object encapsulating the output rows. Supported output formats are:
- `delimited`: Delimited Lines in String format (`parsed_row_sep` parameter must be used to specify the delimiter)
- `fixed-width`: Fixed-width Lines in String format, _Supported only if the `input_row_format` is `fixed-width` type._
- `dict`: Python `dictionary` object, keys will the column names in the provided schema.
- `json`: `Json` data, _Supported only if the `input_row_format` is `json` type and the input data is `Json` data (Python `Dict` is also not supported)._ This constraint is to make sure the serialize-ability of the data.
_**Note Again:** Irrespective of the output data format, the rows/lines will always be in wrapped in Python `Generator` object._
<pre>  
  
</pre>  
**> Special features**,  
> **Parsing Fixed-Width dataset**  
If the source data rows are not delimited like previous case, instead it is fixed width, then use `start` and `end` parameter provided in each parser to mention start and end position for each column while creating the schema, and mention `input_row_format` as **`fixed-width`**. Note `input_row_sep` parameter has no effect in this scenario. Rest of the processes are same. Please checkout following code snippet which handled the act same data in fixed-width format.  
```  
>>> from parseval.parser import StringParser, IntegerParser,DatetimeParser, Parser  
>>> with open('some_file.txt', 'w') as sf:  
>>>       sf.writelines('1MAEVE WILEY  19911024')  
>>>       sf.writelines('2OTIS MILLBURN19920314')  
>>> schema = [  
 ('id', IntegerParser(start=1, end=1, enforce_type=False).not_null()), ('name', StringParser(start=2, end=14, enforce_type=False).not_null().regex_match(r'DEMO\_.*')), ('dob', DatetimeParser(start=15, end=22, formats='%Y%m%d', enforce_type=False).convert('%Y/%m/%d'))]  
>>> parser_obj = Parser(schema=schema,  
 input_row_format = "delimited", parsed_row_format = "json", input_row_sep = "|", stop_on_error=0 )>>> with open('some_file.txt', 'r') as sf:  
>>>    parsed_data = parser_obj.parse(sf)  
>>> for l in parsed_data:  
>>>    print(l)  
{'id': 1, 'name': 'MAEVE WILEY', 'dob': '1991/10/24'}  
{'id': 2, 'name': 'OTIS MILLBURN', 'dob': '1992/03/14'}  
```

**_Note: `start` and `end` are position of the characters(starting with 1, not 0) in the row. Moreover, both positions are included while slicing._** 
<pre>

</pre>
**P.S.:** _It is highly recommended to checkout the example codes provided in the repository to understand the usage more clearly._
<pre>  
  
  
  
  
</pre>  
---  
---  
**_That's all from my end. Hope you find the library useful in your daily data engineering. Please reach out for any queries or suggestion. Feel free to use and enrich the code. I am always avaiable at saumalya75@gmail.com and **linkedin.com/in/saumalya-sarkar-b3712817b_**