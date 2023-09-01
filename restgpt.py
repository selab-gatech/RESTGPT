from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.llms import OpenAI
from langchain.prompts.example_selector import LengthBasedExampleSelector
from specification_parser import parse_parameters
from examples import OPERATION_CONSTRAINT_EXAMPLES
from config import API_KEY

class FewShotModel:
    def __init__(self, examples, prefix, suffix, llm):
        self.examples = examples
        self.prefix = prefix
        self.suffix = suffix
        self.llm = llm

    def run_model(self, input_value):

        print(input_value)

        examples_format = PromptTemplate(
            input_variables=["input", "output"],
            template="Input: {input}\nOutput: {output}"
        )

        examples_selector = LengthBasedExampleSelector(
            examples=self.examples,
            example_prompt=examples_format,
            max_length="5000"
        )
        fewshot_prompt = FewShotPromptTemplate(
            example_prompt=examples_format,
            example_selector=examples_selector,
            example_separator="\n\n",
            prefix=self.prefix,
            suffix=self.suffix,
            input_variables=["input"]
        )

        dependency_chain = LLMChain(prompt=fewshot_prompt, llm=self.llm)

        if isinstance(input_value, list):
            #print(fewshot_prompt.format(input=input_value[0]))
            return dependency_chain.apply(input_value)
        else:
            return dependency_chain.run(input_value)

def operation_constraint(llm, parameters=None):

    input_list = []
    for parameter in parameters:
        name = parameter["name"]
        description = parameter["description"]
        required = parameter["required"]
        if not required:
            input_list.append({"input": f"""name: {name}\ndescription: {description}"""})

    operation_constraint_examples = OPERATION_CONSTRAINT_EXAMPLES

    operation_constraint_prefix = """
Identify the API parameter objects by the grouping of its "name" and "description". Analyze the parameter description 
and determine whether it falls under the following cases where assigned logical operators are applied. Evaluate each
case and determine whether it applies. Be strict with the description wording and make no inferences. Only consider the 
description as mentioning requirements when strong words like "required" and "necessary" are used. Assume Case 1 unless
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

    operation_constraint_suffix = """
Input:\n{input}
Output:\n"""

    dependency_model = FewShotModel(operation_constraint_examples, operation_constraint_prefix,
                                    operation_constraint_suffix, llm)

    return dependency_model.run_model(input_list)

#def parameter_type(llm, parameters):
#
#    input_list = []
#    for parameter in parameters:
#        name = parameter["name"]
#        description = parameter["description"]
#        required = parameter["required"]
#        if not required:
#            input_list.append({"input": f"""name: {name}\ndescription: {description}"""})

#def parameter_constraint(llm, parameters):

def run_llm_chain(file_path, method_path, method_type):

    llm = OpenAI(openai_api_key = API_KEY, temperature=0)

    parameters = parse_parameters(file_path)

    method_key = f"{method_path} {method_type}"
    parameters = parameters.get(method_key)

    operational_constraints = operation_constraint(llm, parameters)
    print(operational_constraints)


if __name__ == "__main__":
    run_llm_chain("specifications/openapi_yaml/spotify.yaml", "/playlists/{playlist_id}/tracks", "get")
