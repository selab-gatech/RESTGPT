MODEL_SUFFIX = """
Input:\n{input}
Output:\n"""

OPERATION_CONSTRAINT_CONTEXT = """
Identify the API parameter object by the grouping of its "name" and "description". Analyze the parameter description 
and determine whether it falls under the following cases where assigned logical operators are applied. Evaluate each
case and determine whether it applies. Be strict with the description wording and make no inferences. Only consider the 
description as requirements when strong words like "required" and "necessary" are used. Interpret the description in the least constraining manner, and assume Case 1 unless
the other cases are obvious: 

Case 1: The description isn't definitive about parameter requirements. Output "None".
Case 2: The description says the parameter is not required. Output "![name]".
Case 3: The description says the parameter is required. Output "name".
Case 4: The description says the parameter and another parameter are required. Output "[name1] & [name2]".
Case 5: The description says the parameter or another parameter are required (inclusive or). Output "[name1] | [name2]".
Case 6: The description says only the parameter or another parameter are required (exclusive or). Output "[name1] ^ [name2]".
 
If there are multiple parameter dependencies in the description, use parantheses and combine them with the logical
operators.

Here are examples of inputs and expected outputs: 
"""

CLASSIFICATION_CONTEXT = """
Classify whether the provided parameter description for an API parameter matches the following categories defined as
"check_operation_constraint", "check_parameter_format", "check_parameter_constraint", and "check_parameter_example",
and return True or False accordingly. Ignore links as irrelevant.\n"""

PARAMETER_FORMAT_CONTEXT = """
Analyze the provided API parameter description and determine whether it clearly identifies the parameter's data type 
or formatting. The list of possible data types are as follows: string, number, integer, boolean, array, and object.
The list of formatting options are as follows: time, date, password, byte, binary, email, uuid, uri, url, hostname,
ipv4, and ipv6. Use the types and formats available for the OpenAPI Specification. If the data type is an array, attempt
to identify its item type. Output the answer as follows: "type [type], items [item type], format [format]". Output
None when unable to determine any of the categories. For example, only output a non-None "item type" if the "type" is 
array.

Here are some examples of inputs and expected outputs:
"""

PARAMETER_CONSTRAINT_CONTEXT = """
Analyze the provided API parameter description and determine whether it describes a restriction of the parameter's 
minimum, maximum possible values. If it does, output in the following format: "min [minimum], max [maximum]". If there  
is no mention of the parameter's minimum and maximum possible values, output "min None, max None".

Here are some examples of inputs and expected outputs:
"""

PARAMETER_EXAMPLE_CONTEXT = """
Analyze the provided API parameter description and determine if there are example values for the parameter, such as 
language codes or country codes. If there are, extrapolate the possible parameter values with the same pattern 
and list them with commas separating them. If the parameter example is not specific or the scope is too large, such as 
"any decimal number" for example, then output "None". If unable to determine any example values, output "None".

Here are some examples of inputs and expected outputs:  
"""