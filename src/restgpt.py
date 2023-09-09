import openai.error
import langchain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.example_selector import LengthBasedExampleSelector
from langchain.output_parsers import PydanticOutputParser
from langchain.cache import InMemoryCache
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from pydantic import BaseModel, Field
from parsers.specification_parser import parse_parameters
from model_properties.examples import *
from model_properties.contexts import *
from config import API_KEY
import time

class Classifications(BaseModel):
    check_operation_constraint: bool = Field(description="""
A boolean that returns True if the input definitively mentions parameters that are required or not required.""")
    check_parameter_format: bool = Field(description="""
A boolean that returns True if the input mentions parameter data types or how the parameter is expected to 
be formatted. Data types and formatting can include lists, dates, numbers, emails, binary, ipv6, among others.""")
    check_parameter_constraint: bool = Field(description="""
A boolean that returns True if the input mentions a limitation of the value of the parameter, such as 
a maximum, minimum, or length.""")
    check_parameter_example: bool = Field(description="""
A boolean that returns True if the input mentions any sample values for the parameter or patterns for the 
parameter value to conform to.""")

class FewShotModel:
    def __init__(self, examples, prefix, suffix, llm):
        self.examples = examples
        self.prefix = prefix
        self.suffix = suffix
        self.llm = llm
        self.examples_format = PromptTemplate(
            input_variables=["input", "output"],
            template="Input: {input}\nOutput: {output}"
        )
        self.examples_selector = LengthBasedExampleSelector(
            examples=self.examples,
            example_prompt=self.examples_format,
            max_length="2048"  # based on words (~7000 word input limit)
        )
        self.fewshot_prompt = FewShotPromptTemplate(
            example_prompt=self.examples_format,
            example_selector=self.examples_selector,
            example_separator="\n\n",
            prefix=self.prefix,
            suffix=self.suffix,
            input_variables=["input"]
        )
        self.fewshot_chain = LLMChain(prompt=self.fewshot_prompt, llm=self.llm)


    def run_model(self, input_value):
        retries = 3
        for i in range(retries):
            try:
                #print(self.fewshot_prompt.format(input=input_value))
                output = self.fewshot_chain.run(input=input_value)
                return output
            except openai.error.OpenAIError as e:
                print(f"Received an API error. Will retry in 20 seconds.")
                time.sleep(20)
        return "None"

def rule_classification(llm, description):
    output_parser = PydanticOutputParser(
        pydantic_object=Classifications
    )
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

def operation_constraint(llm, input_value):
    return FewShotModel(IDL_OPERATION_CONSTRAINT_EXAMPLES, IDL_OPERATION_CONSTRAINT_CONTEXT, MODEL_SUFFIX, llm).run_model(input_value)

def parameter_format(llm, input_value):
    return FewShotModel(PARAMETER_FORMAT_EXAMPLES, PARAMETER_FORMAT_CONTEXT, MODEL_SUFFIX, llm).run_model(input_value)

def parameter_constraint(llm, input_value):
    return FewShotModel(PARAMETER_CONSTRAINT_EXAMPLES, PARAMETER_CONSTRAINT_CONTEXT, MODEL_SUFFIX, llm).run_model(input_value)

def parameter_example(llm, input_value):
    return FewShotModel(PARAMETER_EXAMPLE_EXAMPLES, PARAMETER_EXAMPLE_CONTEXT, MODEL_SUFFIX, llm).run_model(input_value)

def llm_output_formatting(name, specifier, operation_constraints, parameter_formats, parameter_constraints, parameter_examples):
    return {"name": name,
     "specifier": specifier,
     "operational_constraints": operation_constraints,
     "parameter_formats": parameter_formats,
     "parameter_constraints": parameter_constraints,
     "parameter_examples": parameter_examples
     }

def run_llm_chain(file_path, method_path, method_type):

    langchain.llm_cache = InMemoryCache()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", max_tokens=2048, openai_api_key = API_KEY, temperature=0.2, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])

    method_key = f"{method_path} {method_type}"
    parameters = parse_parameters(file_path).get(method_key)

    restriction_list = []
    def run_parameter(parameter):
        parameter_formats = None
        parameter_examples = None
        name = parameter.get("name")
        description = parameter.get("description")
        format_value = parameter.get("format")
        type_value = parameter.get("type")
        enum = parameter.get("enum")
        specifier = parameter.get("specifier")

        if description is None:
            return llm_output_formatting(
                name=name,
                specifier=specifier,
                operation_constraints="None",
                parameter_formats="None",
                parameter_constraints="None",
                parameter_examples="None")

        input_value = f"name: {name}\ndescription: {description}"
        #print("Started operation and parameter constraints")
        operation_constraints = operation_constraint(llm, input_value)
        parameter_constraints = parameter_constraint(llm, description)
        if format_value is None or type_value is None:
            parameter_formats = parameter_format(llm, description)
        if enum is None:
            parameter_examples = parameter_example(llm, description)
        #print("Constraints finished")
        return llm_output_formatting(name=name,
                                     specifier=specifier,
                                     operation_constraints=operation_constraints,
                                     parameter_formats=parameter_formats,
                                     parameter_constraints=parameter_constraints,
                                     parameter_examples=parameter_examples)
    
    for parameter in parameters:
        print(f"Attempting to request from LLM for {parameter}")
        restriction_list.append(run_parameter(parameter))
        print("Completed a restriction!")
        #time.sleep(10)
        #print({operation_constraints, parameter_formats, parameter_constraints, parameter_examples})
    return restriction_list

if __name__ == "__main__":
    print(str(run_llm_chain("specifications/openapi_yaml/youtube.yaml", "/search", "get")))
