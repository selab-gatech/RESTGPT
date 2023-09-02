from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.llms import OpenAI
from langchain.prompts.example_selector import LengthBasedExampleSelector
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from specification_parser import parse_parameters
from model_properties.examples import *
from model_properties.contexts import *
from config import API_KEY
import json

class Classifications(BaseModel):
    check_operation_constraint: bool = Field(description="""
A boolean that returns True if the input definitively mentions parameters that required or not required.""")
    check_parameter_format: bool = Field(description="""
A boolean that returns True if the input mentions parameter data types or how the parameter is expected to 
be formatted.""")
    check_parameter_constraint: bool = Field(description="""
A boolean that returns True if the input mentions a limitation of the value of the parameter, such as 
a maximum, minimum, or length.""")
    check_parameter_example: bool = Field(description="""
A boolean that returns True if the input mentions values for the parameter which it should relate to.""")

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
            max_length="5500" # based on words (~7000 word input limit)
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

def rule_classification(llm, description):

    output_parser = PydanticOutputParser(pydantic_object=Classifications)
    classification_prompt = PromptTemplate(
        template=CLASSIFICATION_CONTEXT + "\n{instructions}\nInput: {description}\n",
        input_variables=["description"],
        partial_variables={"instructions": output_parser.get_format_instructions()}
    )
    rule_classifier = LLMChain(
        llm=llm,
        prompt=classification_prompt,
    )
    return rule_classifier.run(description)

def operation_constraint(llm, parameters=None):

    input_list = []
    for parameter in parameters:
        name = parameter["name"]
        description = parameter["description"]
        required = parameter["required"]
        if not required:
            input_list.append({"input": f"""name: {name}\ndescription: {description}"""})

    operation_constraint_examples = OPERATION_CONSTRAINT_EXAMPLES

    operation_constraint_prefix = OPERATION_CONSTRAINT_CONTEXT

    operation_constraint_suffix = """
Input:\n{input}
Output:\n"""
    dependency_model = FewShotModel(operation_constraint_examples, operation_constraint_prefix,
                                    operation_constraint_suffix, llm)
    input_list = json.dumps(input_list)
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

    llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key = API_KEY, temperature=0)

    method_key = f"{method_path} {method_type}"
    parameters = parse_parameters(file_path).get(method_key)

    operational_constraints = operation_constraint(llm, parameters)
    print(operational_constraints)

    # for parameter in parameters:
    #     rule_classification(llm, parameter["description"])


if __name__ == "__main__":
    run_llm_chain("specifications/openapi_yaml/spotify.yaml", "/playlists/{playlist_id}/tracks", "get")
