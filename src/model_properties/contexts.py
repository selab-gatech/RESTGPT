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

IDL_OPERATION_CONSTRAINT_CONTEXT = """
Identify the API parameter object by the grouping of its "name" and "description". Analyze the parameter description and extract logical constraints
in the provided format. Evaluate each case and determine whether it is applicable. Strictly follow the format and make no inferences. Only consider constraints
that are strictly required. Interpret the description in the least constraining manner, and assume Case 1 unless the other cases are obvious:

Case 1: The description isn't definitive about parameter requirements. Output "None".
Case 2: The description states the parameter "name" is required. Output: "REQUIRED: name". 
Case 3: The description states that parameter "name" or another parameter "name" is required. Output: "Or(name, name)"
Case 4: The description states that given a set of parameters name, name_2, . . . , name_n, zero or one can be present in the API call: Output: "ZeroOrOne(name, name_2, ... name_n)"
Case 5: The description states that given a set of parameters name, name_2, . . . , name_n, exactly one must be present in the API call: Output: "OnlyOne(name, name_2, ... name_n)"
Case 6: The description states that given a set of parameters name, name_2, . . . , name_n, all of them or none must be present in the API call: Output: "AllOrNone(name, name_2, ... name_n)"
Case 7: The description states that there is a relational relationship between some parameters: Output: "name >= name_2", where the standard relational operators can be used
Case 8: The description states that there is an arithmetic relationship between the value of parameters: Output: "name_1 + name_2 <= value", where the standard arithmetic operators can be used
Case 9: The description states there is a conditional relationship between parameters: Output: "IF name THEN name_2", where the standard logical operators can be used
Case 10: The description states that there exists a complex relationship between parameters, you can combine rules from the grammar to express a statement: Output: "IF name==value THEN OnlyOne(name_2 AND name_3, name_4 AND name_5);

The grammar for statements is succinctly defined as follows:

Model:
    Dependency*;
Dependency:
    RelationalDependency | ArithmeticDependency |
    ConditionalDependency | PredefinedDependency;
RelationalDependency:
    Param RelationalOperator Param;
ArithmeticDependency:
    Operation RelationalOperator DOUBLE;
Operation:
    Param OperationContinuation |
    '(' Operation ')' OperationContinuation?;
OperationContinuation:
    ArithmeticOperator (Param | Operation);
ConditionalDependency:
    'IF' Predicate 'THEN' Predicate;
Predicate:
    Clause ClauseContinuation?;
Clause:
    (Term | RelationalDependency | ArithmeticDependency
    | PredefinedDependency) | 'NOT'? '(' Predicate ')';
Term:
    'NOT'? (Param | ParamValueRelation);
Param:
    ID | '[' ID ']';
ParamValueRelation:
    Param '==' STRING('|'STRING)* |
    Param 'LIKE' PATTERN_STRING | Param '==' BOOLEAN |
    Param RelationalOperator DOUBLE;
ClauseContinuation:
    ('AND' | 'OR') Predicate;
PredefinedDependency:
    'NOT'? ('Or' | 'OnlyOne' | 'AllOrNone' |
    'ZeroOrOne') '(' Clause (',' Clause)+ ')';
RelationalOperator:
    '<' | '>' | '<=' | '>=' | '==' | '!=';
ArithmeticOperator:
    '+' | '-' | '*' | '/';

If there are multiple dependency statements, return each one on a new line. Do not include any other text. Do not create dependencies on expected API responses.
Here are some examples of expected outputs:
"""

CLASSIFICATION_CONTEXT = """
Classify whether the provided parameter description for an API parameter matches the following categories defined as
"check_operation_constraint", "check_parameter_format", "check_parameter_constraint", and "check_parameter_example",
and return True or False accordingly. Ignore links as irrelevant. Be lenient with wording and ensure more 
false positives than negatives.\n"""

PARAMETER_FORMAT_CONTEXT = """
Analyze the provided API parameter description and determine whether it clearly identifies the parameter's data type or formatting. 
The list of possible data types are as follows: string, number, integer, boolean, array, and object.
The list of example formatting options are as follows: time, date, password, byte, binary, email, uuid, uri, url, hostname, ipv4, and ipv6. Use the types and formats available for the OpenAPI Specification. 
If the data type is an array, attempt to identify its item type which can be a string, number, integer, boolean, array, or object.
If the data type is an array, attempt to identify its collection format. The list of collection formats are csv (comma-separated values), ssv (space-separated values), psv (pipe-separated values), and tsv (tab-separated values).
Output the answer as follows: "type [type], items [item type], format [format], collectionFormat [collection format]". 
Output None when unable to determine any of the categories. For example, only output a non-None "item type" and "collection type" if the "type" is array. 

Here are some examples of inputs and expected outputs:
"""

PARAMETER_CONSTRAINT_CONTEXT = """
Analyze the provided API parameter description and first estimate the parameter type. Then, according to the type, 
apply the following to determine restrictions on the parameter input:
If it is a number, determine if the description mentions minimum or maximum possible values and output: "min [minimum], max [maximum]". 
If it's a string or word, determine if the description mentions minimum or maximum possible input lengths, and output: "minLength [minimum], maxLength [maximum]". 
If it's an array or list, determine if the description mentions minimum or maximum possible list lengths, and output: "minItems [minimum], maxItems [maximum]".
If it's an object, determine if the description mentions minimum or maximum possible numbers of object properties, and 
output: "minProperties [minimum], maxProperties [maximum]".
If you are unable to determine any minimum or maximum restrictions, output "None". If you are able to determine only one 
either the minimum or maximum, output the undetermined value as "None".

Here are some examples of inputs and expected outputs:
"""

PARAMETER_EXAMPLE_CONTEXT = """
Analyze the provided API parameter description, and extract any example values for the parameter mentioned in the description. 
Then, generate a few additional example values that correspond to, or are in the same category as the provided values.
If there are no example values provided, simply generate values corresponding to the description, and always generate values when possible.  
Do not generate examples of number ranges at all, and return None in that case. 
If generating example values is not possible, return None. Consider the following cases: 

Case 1: The description contains example values USA, CAN, ZWE: Output: "PROVIDED: USA, CAN, ZWE +++ GENERATED: BRA, FRA, GER ..."
Case 2: The description does not explicitly mention example values: Output: "PROVIDED: None +++ GENERATED: BRA, FRA, GER, USA ..."
Case 3: The description does not explicitly mention example values, and it is not possible to generate example values: Output: "None"

Here are some examples of inputs and expected outputs:"""