from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.llms import OpenAI
from langchain.prompts.example_selector import LengthBasedExampleSelector
from specification_parser import parse_parameters
from config import API_KEY

def operation_constraint(llm, parameters=None):

    input_list = []
    for parameter in parameters:
        name = parameter["name"]
        description = parameter["description"]
        required = parameter["required"]
        if not required:
            input_list.append({"input": f"""name: {name}\ndescription: {description}"""})

    dependency_examples = [
        {
            "input": """
name: text
description: 'The text to be checked. This or 'data' is required.'""",
            "output": "text|data"
        },
        {
            "input": """
name: bidSelectionMethod
description: 'alid examples are Đấu thầu rộng rãi, Đấu thầu hạn chế, etc...'""",
            "output": "None"
        },
        {
            "input": """
name: idea
description: 'An idea for a project. This and 'rating' are required.'""",
            "output": "idea&rating"
        },
        {
            "input": """
name: day
description: 'The current day that the letter grade is being published'""",
            "output": "None"
        },
        {
            "input": """
name: comment
description: 'Use with 'username' to define a post.'""",
            "output": "None"
        },

    ]

    dependency_prefix = """
Identify the API parameter objects by the grouping of its "name" and "description". Analyze the parameter description 
and determine whether it falls under the following cases where assigned logical operators are applied. Evaluate each
case and determine whether it applies. Assume Case 1 and output "None" if no other cases apply. Be strict with the description
wording and make no inferences. Only consider the description as mentioning requirements when strong words like 
"required" and "necessary" are used: 

Case 1: The description mentions nothing definitive for parameter requirements for the API. Output "None".
Case 2: The description says the parameter is not required. Output "![name]".
Case 3: The description says the parameter is required. Output "name".
Case 4: The description says the parameter and another parameter are required. Output "[name1] & [name2]".
Case 5: The description says the parameter or another parameter are required (inclusive or). Output "[name1] | [name2]".
Case 6: The description says either the parameter or another parameter are required (exclusive or). Output "[name1] ^ [name2]".
 
If there are multiple parameter dependencies in the description, use parantheses and combine them with the logical
operators.

Here are examples of input and output pairs: """

    dependency_suffix = """
Input:\n{input}
Output:\n"""

    dependency_format = PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nOutput: {output}"
    )

    dependency_selector = LengthBasedExampleSelector(
        examples=dependency_examples,
        example_prompt=dependency_format,
        max_length="5000"
    )
    dependency_fewshot_prompt = FewShotPromptTemplate(
        example_prompt=dependency_format,
        example_selector=dependency_selector,
        example_separator="\n\n",
        prefix=dependency_prefix,
        suffix=dependency_suffix,
        input_variables=["input"]
    )

    dependency_chain = LLMChain(prompt=dependency_fewshot_prompt, llm=llm)

    #print(dependency_fewshot_prompt.format(input=input_list))
    return dependency_chain.apply(input_list)

#def parameter_type(llm, parameters):
#
#    input_list = []
#    for parameter in parameters:
#        name = parameter["name"]
#        description = parameter["description"]
#        required = parameter["required"]
#        if not required:
#            input_list.append({"input": f"""name: {name}\ndescription: {description}"""})



def parameter_constraint(llm, parameters):

    rule_examples = [
        {
            "input": """
    paths: /search:
      get:
        operationId: Web_Search 
          parameters:
          - name: Accept-Language
            in: header
            type: string
            description: A comma-delimited list of one or more languages to use for user interface strings.
          - name: count
            in: query
            type: integer
            format: int32
            description: The maximum value is 50.""",
            "output": """
    Name: Accept-Language
    Rules: A list of strings containing at least one element representing languages.

    Name: count
    Rules: An integer of maximum value 50."""
        },
        {
            "input": "test",
            "output": "test"
        }
    ]

    rule_prefix = """
    You are attempting to decipher rules from the 'description' field for each parameter of a yaml file. The following 
    are some examples of determining limitations on data types and values that you will imitate:
        """

    rule_suffix = """
    input: {input}
    output:
        """

    rule_example_format = PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nOutput: {output}"
    )

    rule_example_selector = LengthBasedExampleSelector(
        examples=rule_examples,
        example_prompt=rule_example_format,
        max_length="1000"
    )

    rule_fewshot_prompt = FewShotPromptTemplate(
        example_prompt=rule_example_format,
        example_selector=rule_example_selector,
        example_separator="\n\n",
        prefix=rule_prefix,
        suffix=rule_suffix,
        input_variables=["input"]
    )

    rule_chain = LLMChain(prompt=rule_fewshot_prompt, llm=llm)

    # print(rule_fewshot_prompt.format(input="Test fewshot prompt input"))

def run_llm_chain(file_path, method_path, method_type):

    llm = OpenAI(openai_api_key = API_KEY, temperature=0)

    parameters = parse_parameters(file_path)

    method_key = f"{method_path} {method_type}"
    parameters = parameters.get(method_key)

    operational_constraints = operation_constraint(llm, parameters))


if __name__ == "__main__":
    run_llm_chain("specifications/openapi_yaml/spotify.yaml", "/search", "get")
