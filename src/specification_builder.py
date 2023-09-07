from restgpt import run_llm_chain
from parsers.ipd_parser import InterDependencyParser
from prance import ResolvingParser, BaseParser
from parsers.parameter_constraint_parser import ParameterConstraintParser
from parsers.example_parser import InputParser
from parsers.parameter_format_parser import ParameterFormatParser
from parsers.specification_parser import parse_parameters
import json

class SpecificationBuilder:
    def __init__(self, read_path, output_path):
        self.operation_constraint_parser = InterDependencyParser()
        self.example_parser = InputParser()
        self.parameter_format_parser = ParameterFormatParser()
        self.parameter_constraint_parser = ParameterConstraintParser()
        self.output_builder = BaseParser(read_path).specification
        self.read_path = read_path
        self.output_path = output_path

    def add_parameter_constraint(self, parameter, parameter_constraint):
        for min_max, value in parameter_constraint.items():
            parameter[min_max] = value
    
    def build_constraint(self, method_path, parameter_name, operation_constraint, example_constraint, format_constraint, parameter_constraint):
        path_values = self.output_builder.get("paths", {}).get(method_path)
        for method_type, method_values in path_values.items():
            parameters = method_values.get("parameters", {})
            for parameter in parameters:
                if parameter.get("name") == parameter_name:
                    self.add_parameter_constraint(parameter.get("schema"), parameter_constraint)

        with open("test_output.json", 'w') as file:
            result = self.output_builder
            json.dump(result, file, indent=4)
        #for path, path_values in self.output_builder.items():
            #for method_type, method_values in path_values.items(): # Determine HTTP method
                #print(method_values)

    def find_constraints(self, method_path, method_type):
        model_output = run_llm_chain(self.read_path, method_path, method_type)
        for parameter in model_output:
            operation_constraint = self.operation_constraint_parser.parse_parameter(parameter.get("operation_constraints"))
            example_constraint = self.example_parser.parse_examples(parameter.get("parameter_examples"))
            format_constraint = self.parameter_format_parser.parse(parameter.get("parameter_formats"))
            parameter_constraint = self.parameter_constraint_parser.parse(parameter.get("operational_constraints"))
            #print(str(operation_constraint))
            #print(str(example_constraint))
            #print(str(format_constraint))
            #print(str(parameter_constraint))



        return model_output

    def output_specifications(self):
        for method_key, description_value in parse_parameters(self.read_path).items():
            method_values = method_key.split(" ")
            method_path = method_values[0]
            method_type = method_values[1]
            self.find_constraints(method_path, method_type)

if __name__ == "__main__":
    specification_builder = SpecificationBuilder("specifications/openapi_yaml/spotify.yaml", "outputs/spotify.yaml")
    #print(str(specification_builder.find_constraints("/me/playlists", "get")))
    print(str(specification_builder.build_constraint("/me/playlists", "limit", None, None, None, {"min": 100, "max": 1200})))
    #specification_builder.output_specifications()