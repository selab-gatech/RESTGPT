OPERATION_CONSTRAINT_CONTEXT = """
Identify the API parameter objects by the grouping of its "name" and "description". Analyze the parameter description 
and determine whether it falls under the following cases where assigned logical operators are applied. Evaluate each
case and determine whether it applies. Be strict with the description wording and make no inferences. Only consider the 
description as requirements when strong words like "required" and "necessary" are used. Interpret the description in the least constraining manner, and assume Case 1 unless
the other cases are obvious: 

Case 1: The description isn't definitive about parameter requirements. Output "None".
Case 2: The description says the parameter is not required. Output "![name]".
Case 3: The description says the parameter is required. Output "name".
Case 4: The description says the parameter and another parameter are required. Output "[name1] & [name2]".
Case 5: The description says the parameter or another parameter are required (inclusive or). Output "[name1] | [name2]".
Case 6: The description says either the parameter or another parameter are required (exclusive or). Output "[name1] ^ [name2]".
 
If there are multiple parameter dependencies in the description, use parantheses and combine them with the logical
operators.

Here are examples of input and output pairs: """

CLASSIFICATION_CONTEXT = """
Classify whether the provided parameter description for an API parameter matches the following categories defined as
"check_operation_constraint", "check_parameter_format", "check_parameter_constraint", and "check_parameter_example",
and return True or False accordingly. Ignore links as irrelevant.\n"""