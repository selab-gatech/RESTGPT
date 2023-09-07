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
        self.output_builder = ResolvingParser(read_path).specification
        self.read_path = read_path
        self.output_path = output_path

    def add_parameter_constraint(self, parameter, parameter_constraint):
        correct_mappings = {"min": "number", "max": "number", "minItems": "array", "maxItems": "array"}
        mapping_key = parameter.get("type") if parameter.get("type") != "integer" else "number"
        for min_max, value in parameter_constraint.items():
<<<<<<< HEAD
            parameter[min_max] = value
    
    def build_constraint(self, method_path, parameter_name, operation_constraint, example_constraint, format_constraint, parameter_constraint):
=======
            if correct_mappings.get(min_max) == mapping_key:
                if value.strip() is not "None":
                    parameter.setdefault(min_max, value)
            else:
                return

    def add_format_constraint(self, parameter, format_constraint):
        parameter.setdefault("type", format_constraint.get("type"))
        if parameter.get("type") == "array":
            parameter.setdefault("items", {})
            parameter.get("items", {}).setdefault("type", format_constraint.get("items"))
            parameter.get("items", {}).setdefault("format", format_constraint.get("format"))
        else:
            parameter.setdefault("format", format_constraint.get("format"))

    def process_parameters(self, method_values, parameter_name, example_constraint, format_constraint, parameter_constraint):
        for parameter in method_values.get("parameters", []):
            if parameter.get("name") == parameter_name:
                if parameter_constraint is not None:
                    self.add_parameter_constraint(parameter.get("schema", {}), parameter_constraint)
                if format_constraint is not None:
                    self.add_format_constraint(parameter.get("schema", {}), format_constraint)
    def process_requestBody(self, method_values, parameter_name, example_constraint, format_constraint, parameter_constraint):
        for encoding, encoding_values in method_values.get("requestBody", {}).get("content", {}).items():
            for property_name, attributes in encoding_values.get("schema", {}).get("properties", {}).items():
                if property_name == parameter_name:
                    self.add_parameter_constraint(attributes, parameter_constraint)

    # def add_operational_constraint(self, parameter, operation_constraint):

    def build_constraint(self, method_path, parameter_name, specification, example_constraint, format_constraint, parameter_constraint):
>>>>>>> a324dad1336ba9c2852a4be1f08842378f7ccece
        path_values = self.output_builder.get("paths", {}).get(method_path)
        for method_type, method_values in path_values.items():
            if specification == "parameter":
                self.process_parameters(method_values, parameter_name, example_constraint, format_constraint, parameter_constraint)
            elif specification == "requestBody":
                self.process_requestBody(method_values, parameter_name)

        with open("test_output.json", 'w') as file:
            result = self.output_builder
            json.dump(result, file, indent=4)

    def find_constraints(self, method_path, method_type):
        model_output = run_llm_chain(self.read_path, method_path, method_type)
        for parameter in model_output:
            specifier = parameter.get("specifier")
            operation_constraint = self.operation_constraint_parser.parse_parameter(parameter.get("operation_constraints"))
            example_constraint = self.example_parser.parse_examples(parameter.get("parameter_examples"))
            format_constraint = self.parameter_format_parser.parse(parameter.get("parameter_formats"))
<<<<<<< HEAD
            parameter_constraint = self.parameter_constraint_parser.parse(parameter.get("operational_constraints"))
=======
            parameter_constraint = self.parameter_constraint_parser.parse(parameter.get("parameter_constraints"))
            self.build_constraint(method_path, specifier, parameter.get("name"), example_constraint, format_constraint, parameter_constraint)
>>>>>>> a324dad1336ba9c2852a4be1f08842378f7ccece
            #print(str(operation_constraint))
            #print(str(example_constraint))
            #print(str(format_constraint))
            #print(str(parameter_constraint))

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