from src.llm import run_llm_chain
from prance import ResolvingParser
from src.parsers.parameter_constraint_parser import ParameterConstraintParser
from src.parsers.example_parser import ExampleParser
from src.parsers.parameter_format_parser import ParameterFormatParser
from src.parsers.specification_parser import parse_parameters
from src.parsers.ipd_parser import InterDependencyParser
from typing import *
from src.model_properties.contexts import *
from src.model_properties.examples import *
import yaml
import json
import os


class Parameter_Example:
    def __init__(self, provided=None, generated=None, valid=False):
        self.provided = provided
        self.generated = generated
        self.valid = valid


class Parameter_Constraint:
    def __init__(self, min=None, max=None, minLength=None, maxLength=None, minItems=None, maxItems=None,
                 minProperties=None, maxProperties=None, default=None, valid=False):
        self.min = min
        self.max = max
        self.minLength = minLength  # Ensure this is treated as an integer
        self.maxLength = maxLength  # Ensure this is treated as an integer
        self.minItems = minItems
        self.maxItems = maxItems
        self.minProperties = minProperties
        self.maxProperties = maxProperties
        self.default = default
        self.valid = valid


class Parameter_Format:
    def __init__(self, type=None, format=None, collectionFormat=None, items=None, valid=False):
        self.type = type
        self.format = format
        self.collectionFormat = collectionFormat
        self.items = items
        self.valid = valid


class Operation_Constraint:
    def __init__(self, x_dependencies=None, valid=False):
        self.x_dependencies = x_dependencies
        self.valid = valid


class LLM_CSV_Body:
    def __init__(self, parameter: str, temperature: float, token_limit: int, prompt: str, response: str):
        self.parameter = parameter
        self.temperature = temperature
        self.token_limit = token_limit
        self.prompt = prompt
        self.response = response


class SpecificationBuilder:
    def __init__(self, read_path, output_path=None):
        self.ipd_parser = InterDependencyParser()
        self.example_parser = ExampleParser()
        self.parameter_constraint_parser = ParameterConstraintParser()
        self.parameter_format_parser = ParameterFormatParser()
        self.output_builder = ResolvingParser(read_path,
                                              strict=False).specification
        self.read_path = read_path
        self.output_path = output_path
        self.paths = []
        valid_http_methods = {'put', 'post', 'patch', 'get', 'delete', 'options', 'head', 'patch', 'trace'}
        for path, path_values in self.output_builder.get('paths', {}).items():
            for method_type, method_values in path_values.items():
                if method_type in valid_http_methods:
                    method_key_tuple = (path, method_type)
                    self.paths.append(method_key_tuple)
        self.parsed_parameters = parse_parameters(self.read_path)
        self.method_parameter_set = {}
        for method_key, value_list in self.parsed_parameters.items():
            self.method_parameter_set[method_key] = []
            for parameter in value_list:
                if parameter["specifier"] == "parameter":
                    self.method_parameter_set[method_key].append(parameter["name"])
        for method_key in self.parsed_parameters.keys():
            self.method_parameter_set[method_key] = set(self.method_parameter_set[method_key])
        self.report = {}
        self.values_to_add = set(['examples', 'x-dependencies'])

    def _convert_key(self, path):
        return f'{path[0]} {path[1]}'

    def _add_parameter_constraint(self, build_parameter, parameter_constraint):
        if parameter_constraint is None:
            return

        for constraint_key, constraint in parameter_constraint.items():
            if constraint_key in ["minProperties", "maxProperties"] and constraint is not None:
                try:
                    build_parameter[constraint_key] = int(constraint)  # Ensure it's set as an integer.
                except ValueError:
                    pass  # Handle invalid conversion if necessary.
            elif constraint_key in ['max', 'min'] and constraint is not None and "type" in build_parameter:
                if build_parameter["type"] in ["integer", "number"]:
                    build_parameter[constraint_key] = constraint

                    # New line to prevent additional properties
                    build_parameter["additionalProperties"] = False

                else:
                    # Remove max/min if type is not appropriate
                    build_parameter.pop(constraint_key, None)
            elif constraint is not None and constraint.strip() != "None":
                build_parameter[constraint_key] = constraint

    def _add_ipd_constraint(self, build_parameter, ipd_constraint):
        if ipd_constraint is None:
            return
        for constraint in ipd_constraint:
            build_parameter["x-dependencies"] = ipd_constraint[constraint]

    def _add_example_values(self, build_parameter, model_examples):
        if model_examples is None:
            return
        example_key = "examples"
        build_parameter[example_key] = model_examples

    def _add_parameter_type_values(self, build_parameter, parameter_types):
        if parameter_types is None:
            return None
        for type_key, extracted_type in parameter_types.items():
            if extracted_type.strip() != "None":
                if type_key == "items" or type_key == "collectionFormat":
                    if parameter_types["type"] == "array":
                        build_parameter[type_key] = extracted_type
                else:
                    build_parameter[type_key] = extracted_type

    def process_operation(self, path, method):
        operation = None
        if path in self.output_builder['paths']:
            if method in self.output_builder['paths'][path]:
                operation = self.output_builder['paths'][path][method]
        if operation is None:
            raise Exception("Operation not found")
        parameters = None
        xdependencies = []
        request_body = None
        if 'x-dependencies' in operation:
            xdependencies = operation['x-dependencies']
        if 'parameters' in operation:
            parameters = operation['parameters']
        if 'requestBody' in operation:
            if method != 'GET':
              request_body = True
            else:
              request_body = False
        generated_parameter_values, generated_request_body_values = self.model_constraints(path, method)
        if parameters:
            for parameter in parameters:
                self.process_parameter(parameter, generated_parameter_values, xdependencies)
        if request_body:
            self.process_request_body(operation['requestBody'], generated_request_body_values, xdependencies)
        if xdependencies:
            operation['x-dependencies'] = xdependencies

    def process_parameter(self, parameter, generated_parameter_values, xdependencies):
        if parameter['name'] in generated_parameter_values:
            constraint_set = generated_parameter_values[parameter['name']]
            if 'name' in constraint_set:
                constraint_set.pop("name")

            # Ensure 'example' is not included if 'examples' exists
            if 'examples' in constraint_set:
                if 'example' in parameter:
                    del parameter['example']  # Remove the example key

                parameter['examples'] = {}
                for key in constraint_set['examples']['examples']:
                    parameter['examples'][key] = constraint_set['examples']['examples'][key]
                constraint_set.pop("examples")

            elif 'example' in constraint_set:
                # If 'examples' doesn't exist but 'example' does, set it
                parameter['example'] = constraint_set.pop("example")

            if 'x-dependencies' in constraint_set:
                xdependencies.extend(constraint_set['x-dependencies'])
                constraint_set.pop("x-dependencies")

            if 'schema' not in parameter:
                parameter['schema'] = {}

            # Handle the schema and styles
            schema_loc = parameter['schema']
            if 'type' in constraint_set:
                if constraint_set['type'] == 'array':
                    schema_loc.setdefault("items", {})
                    if constraint_set.get("items") is not None and constraint_set.get("items").strip() != "None":
                        schema_loc["items"].setdefault("type", constraint_set.get("items"))

                    if 'maxItems' in constraint_set:
                        schema_loc.setdefault("maxItems", int(constraint_set['maxItems']))  # Keep this as int for items
                    if 'minItems' in constraint_set:
                        schema_loc.setdefault("minItems", int(constraint_set['minItems']))
                    if constraint_set.get("format") is not None and constraint_set.get("format").strip() != "None":
                        schema_loc["items"].setdefault("format", constraint_set.get("format"))
                else:
                    schema_loc.setdefault("type", constraint_set.get("type"))
                    # Handle max and min constraints
                    if 'max' in constraint_set:
                        # Check for float or int, then set accordingly
                        try:
                            if schema_loc["type"] in ["integer", "number"]:
                                schema_loc.setdefault("maximum", int(float(constraint_set['max'])))
                            constraint_set.pop("max", None)
                        except ValueError:
                            # Handle invalid conversion if necessary (either log or ignore)
                            pass

                    if 'min' in constraint_set:
                        # Similarly, handle both integer and float
                        try:
                            if schema_loc["type"] in ["integer", "number"]:
                                schema_loc.setdefault("minimum", int(float(constraint_set['min'])))
                            constraint_set.pop("min", None)
                        except ValueError:
                            # Handle invalid conversion if necessary (either log or ignore)
                            pass

                    constraint_set.pop("type")

            # Set additional constraints
            for field in constraint_set:
                # Here collectionFormat is removed and style/explode
                if field != "collectionFormat":
                    if field in ["minLength", "maxLength"] and constraint_set[field] is not None:
                        constraint_set[field] = int(constraint_set[field])
                    parameter['schema'].setdefault(field, constraint_set.get(field))

    def process_request_body(self, request_body, generated_request_body_values, xdependencies):
        encoding_type = None
        for encoding in request_body.get("content", {}):
            if encoding != 'description':
                encoding_type = encoding
                break
        if encoding_type:
            if 'schema' in request_body['content'][encoding_type]:
                if 'properties' in request_body['content'][encoding_type]['schema']:
                    for property_name in request_body['content'][encoding_type]['schema']['properties']:
                        constraint_set = None
                        for item in generated_request_body_values:
                            if isinstance(item, dict) and 'name' in item and property_name == item['name']:
                                constraint_set = item
                        if constraint_set:
                            # Remove collection format, and add style and explode
                            if 'collectionFormat' in constraint_set:
                                del constraint_set['collectionFormat']

                            if 'name' in constraint_set:
                                constraint_set.pop("name")

                            # Ensure that if we have examples, we remove the example key if it exists
                            if 'examples' in constraint_set:
                                if 'example' in request_body['content'][encoding_type]['schema']['properties'][property_name]:
                                    del request_body['content'][encoding_type]['schema']['properties'][property_name]['example']  # Remove the example key if it exists

                                request_body['content'][encoding_type].setdefault("examples", {})
                                for key in constraint_set['examples']['examples']:
                                    request_body['content'][encoding_type]['examples'][key] = \
                                        constraint_set['examples']['examples'][key]
                                constraint_set.pop("examples")

                            if 'x-dependencies' in constraint_set:
                                xdependencies.extend(constraint_set['x-dependencies'])
                                constraint_set.pop("x-dependencies")

                            if 'type' in constraint_set:
                                if constraint_set['type'] == 'array':
                                    prop_loc = request_body['content'][encoding_type]['schema']['properties'][
                                        property_name]
                                    prop_loc.setdefault("items", {})
                                    if constraint_set.get("items") is not None and constraint_set.get("items").strip() != "None":
                                        prop_loc['items'].setdefault("type", constraint_set.get("items"))
                                    if constraint_set.get("format") is not None and constraint_set.get("format").strip() != "None":
                                        prop_loc['items'].setdefault("format", constraint_set.get("format"))

                                    if 'minItems' in constraint_set:
                                        prop_loc.setdefault("minItems", int(constraint_set['minItems']))
                                    if 'maxItems' in constraint_set:
                                        prop_loc.setdefault("maxItems", int(constraint_set['maxItems']))
                                else:
                                    request_body['content'][encoding_type]['schema']['properties'][property_name].setdefault("type", constraint_set.get("type"))
                                constraint_set.pop("type")

                            for field in constraint_set:
                                if field == "minLength" and constraint_set[field] is not None:
                                    constraint_set[field] = int(constraint_set[field])
                                elif field == "maxLength" and constraint_set[field] is not None:
                                    constraint_set[field] = int(constraint_set[field])
                                request_body['content'][encoding_type]['schema']['properties'][
                                    property_name].setdefault(field, constraint_set.get(field))


    def model_constraints(self, path, method):
        constraint_dict = run_llm_chain(self.read_path, path, method)
        parameters = {}
        request_body = []
        for parameter in constraint_dict:
            parameter_spec = {}
            parameter_spec['name'] = parameter['name']
            self._add_parameter_constraint(parameter_spec,
                                           self.parameter_constraint_parser.parse(parameter["parameter_constraints"]))
            self._add_ipd_constraint(parameter_spec,
                                     self.ipd_parser.parse_parameter(parameter["operational_constraints"]))
            self._add_parameter_type_values(parameter_spec,
                                            self.parameter_format_parser.parse(parameter["parameter_formats"]))
            if parameter["name"] in self.method_parameter_set[self._convert_key((path, method))]:
                self._add_example_values(parameter_spec,
                                         self.example_parser.parse_examples(parameter["parameter_examples"],
                                                                            is_requestBody=False,
                                                                            parameter_name=parameter["name"]))
                parameters[parameter["name"]] = parameter_spec
            else:
                self._add_example_values(parameter_spec,
                                         self.example_parser.parse_examples(parameter["parameter_examples"],
                                                                            is_requestBody=False,
                                                                            parameter_name=parameter["name"]))
                request_body.append(parameter_spec)
        return parameters, request_body

    def make_report_constraint_object(self, path, operation, parameter, values, requestBody):
        restrictions = []
        for value, restrict in values.items():
            if value == "max":
                value = "maximum"
            elif value == "min":
                value = "minimum"

            restrictions.append({
                "restriction_name": value,
                "restriction_value": restrict
            })
        return {
            "path": path,
            "method": operation,
            "parameter": parameter,
            "restrictions": restrictions,
            "request_body": requestBody
        }

    def find_report_constraints(self, report_values):
        constraint_list = []
        for path, method in report_values.items():
            for operation, parameters in method.items():
                for parameter, values in parameters.items():
                    if parameter != "request-body":
                        constraint_list.append(
                            self.make_report_constraint_object(path, operation, parameter, values, False))
                    else:
                        for request_parameter, request_values in values.items():
                            constraint_list.append(
                                self.make_report_constraint_object(path, operation, request_parameter, request_values,
                                                                   True))
        return constraint_list

    def assign_rule_categories(self, restriction_name, restriction_value, parameter_example, parameter_constraint,
                               parameter_format, operation_constraint):
        parameter_example_map = {'provided': 'provided', 'generated': 'generated'}
        parameter_constraint_map = {'minimum': 'min', 'maximum': 'max', 'minLength': 'minLength',
                                    'maxLength': 'maxLength',
                                    'minItems': 'minItems', 'maxItems': 'maxItems', 'minProperties': 'minProperties',
                                    'maxProperties': 'maxProperties', 'default': 'default'}
        parameter_format_map = {'type': 'type', 'format': 'format', 'collectionFormat': 'collectionFormat',
                                'items': 'items'}
        operation_constraint_map = {'x_dependencies': 'x_dependencies'}

        if restriction_name in parameter_example_map:
            setattr(parameter_example, parameter_example_map[restriction_name], restriction_value)
            parameter_example.valid = True
        elif restriction_name in parameter_constraint_map:
            setattr(parameter_constraint, parameter_constraint_map[restriction_name], restriction_value)
            parameter_constraint.valid = True
        elif restriction_name in parameter_format_map:
            setattr(parameter_format, parameter_format_map[restriction_name], restriction_value)
            parameter_format.valid = True
        elif restriction_name in operation_constraint_map:
            setattr(operation_constraint, operation_constraint_map[restriction_name], restriction_value)
            operation_constraint.valid = True

    def llm_example_pair(self, description, parameter_example):
        example_prompt = PARAMETER_EXAMPLE_CONTEXT + "\n"
        for example in PARAMETER_EXAMPLE_EXAMPLES:
            example_input = example["input"]
            example_output = example["output"]
            example_prompt += f"Input:{example_input}\nOutput:{example_output}\n"
        example_prompt += f"Input:{description}\nOutput:"

        example_response = "None"
        if parameter_example.valid:
            example_response = "PROVIDED: "
            if parameter_example.provided is None:
                example_response += "None"
            else:
                for example in parameter_example.provided:
                    example_response += f"{example}, "
                if example_response[-2] == ",":
                    example_response = example_response[:-2]

            example_response += " +++ GENERATED: "
            if parameter_example.generated is None:
                example_response += "None"
            else:
                for example in parameter_example.generated:
                    example_response += f"{example}, "
                if example_response[-2] == ",":
                    example_response = example_response[:-2]

        return example_prompt, example_response

    def llm_constraint_pair(self, description, parameter_constraint, parameter_constraint_type):
        constraint_prompt = PARAMETER_CONSTRAINT_CONTEXT + "\n"
        for example in PARAMETER_CONSTRAINT_EXAMPLES:
            example_input = example["input"]
            example_output = example["output"]
            constraint_prompt += f"Input:{example_input}\nOutput:{example_output}\n"
        constraint_prompt += f"Input:{description}\nOutput:"

        constraint_response = "None"
        if parameter_constraint.valid:
            if parameter_constraint_type == 'int':
                min = parameter_constraint.min if parameter_constraint.min is not None else "None"
                max = parameter_constraint.max if parameter_constraint.max is not None else "None"
                default = parameter_constraint.default if parameter_constraint.default is not None else "None"
                constraint_response = f"min {min}, max {max}, default {default}"
            if parameter_constraint_type == 'string':
                minLength = parameter_constraint.minLength if parameter_constraint.minLength is not None else "None"
                maxLength = parameter_constraint.maxLength if parameter_constraint.maxLength is not None else "None"
                default = parameter_constraint.default if parameter_constraint.default is not None else "None"
                constraint_response = f"minLength {minLength}, maxLength {maxLength}, default {default}"
            if parameter_constraint_type == 'list':
                minItems = parameter_constraint.minItems if parameter_constraint.minItems is not None else "None"
                maxItems = parameter_constraint.maxItems if parameter_constraint.maxItems is not None else "None"
                default = parameter_constraint.default if parameter_constraint.default is not None else "None"
                constraint_response = f"minItems {minItems}, maxItems {maxItems}, default {default}"
            if parameter_constraint_type == 'object':
                minProperties = parameter_constraint.minProperties if parameter_constraint.minProperties is not None else "None"
                maxProperties = parameter_constraint.maxProperties if parameter_constraint.maxProperties is not None else "None"
                default = parameter_constraint.default if parameter_constraint.default is not None else "None"
                constraint_response = f"minProperties {minProperties}, maxProperties {maxProperties}, default {default}"

        return constraint_prompt, constraint_response

    def llm_format_pair(self, description, parameter_format):
        format_prompt = PARAMETER_FORMAT_CONTEXT + "\n"
        for example in PARAMETER_FORMAT_EXAMPLES:
            example_input = example["input"]
            example_output = example["output"]
            format_prompt += f"Input:{example_input}\nOutput:{example_output}\n"
        format_prompt += f"Input:{description}\nOutput:"

        format_response = "None"
        if parameter_format.valid:
            type = parameter_format.type if parameter_format.type is not None else "None"
            items = parameter_format.items if parameter_format.items is not None else "None"
            format = parameter_format.format if parameter_format.format is not None else "None"
            collectionFormat = parameter_format.collectionFormat if parameter_format.collectionFormat is not None else "None"
            format_response = f"type {type}, items {items}, format {format}, collectionFormat {collectionFormat}"

        return format_prompt, format_response

    def llm_operation_pair(self, description, operation_constraint):
        operation_prompt = IDL_OPERATION_CONSTRAINT_CONTEXT + "\n"
        for example in IDL_OPERATION_CONSTRAINT_EXAMPLES:
            example_input = example["input"]
            example_output = example["output"]
            operation_prompt += f"Input:{example_input}\nOutput:{example_output}\n"
        operation_prompt += f"Input:{description}\nOutput:"

        operation_response = "None"
        if operation_constraint.valid:
            if operation_constraint.x_dependencies is None:
                operation_response = "None"
            else:
                operation_response = ""
                for dependency in operation_constraint.x_dependencies:
                    operation_response += f"{dependency}\n"
                if operation_response[-2:] == "\n":
                    operation_response = operation_response[:-2]

        return operation_prompt, operation_response

    def create_prompt_and_response(self, parameter_info: dict):
        description = parameter_info['description']

        parameter_constraint_type = 'int'
        constraint_type_mapping = {
            'minimum': 'int', 'maximum': 'int',
            'minLength': 'string', 'maxLength': 'string',
            'minItems': 'list', 'maxItems': 'list',
            'minProperties': 'object', 'maxProperties': 'object'
        }

        parameter_example = Parameter_Example()
        parameter_constraint = Parameter_Constraint()
        parameter_format = Parameter_Format()
        operation_constraint = Operation_Constraint()

        for restriction in parameter_info['restrictions']:
            restriction_name = restriction['restriction_name']
            restriction_value = restriction['restriction_value']
            if restriction_name in constraint_type_mapping:
                parameter_constraint_type = constraint_type_mapping[restriction_name]
            self.assign_rule_categories(restriction_name, restriction_value, parameter_example, parameter_constraint,
                                        parameter_format, operation_constraint)

        example_prompt, example_response = self.llm_example_pair(description, parameter_example)
        constraint_prompt, constraint_response = self.llm_constraint_pair(description, parameter_constraint,
                                                                          parameter_constraint_type)
        format_prompt, format_response = self.llm_format_pair(description, parameter_format)
        operation_prompt, operation_response = self.llm_operation_pair(description, operation_constraint)

        example_body = LLM_CSV_Body(parameter_info['parameter'], 0.2, 256, example_prompt, example_response)
        constraint_body = LLM_CSV_Body(parameter_info['parameter'], 0.2, 256, constraint_prompt, constraint_response)
        format_body = LLM_CSV_Body(parameter_info['parameter'], 0.2, 256, format_prompt, format_response)
        operation_body = LLM_CSV_Body(parameter_info['parameter'], 0.2, 256, operation_prompt, operation_response)

        return [example_body, constraint_body, format_body, operation_body]

    def generate_llm_query_objects(self, file_path: str) -> List[LLM_CSV_Body]:

        with open(file_path, 'r') as json_file:
            report_values = json.load(json_file)

        constraint_list = self.find_report_constraints(report_values)
        self.add_parameter_description(constraint_list)

        query_objects = []
        for parameter_info in constraint_list:
            for body in self.create_prompt_and_response(parameter_info):
                query_objects.append(body)

        return query_objects

    def process_cast_example(self, example, param_type):
        if param_type is None:
            example.strip("\"")
            return example
        if param_type["is_int"]:
            try:
                return int(example)
            except ValueError:
                return None
        elif param_type["is_float"]:
            try:
                return float(example)
            except ValueError:
                return None
        elif param_type["is_bool"]:
            try:
                return bool(example)
            except ValueError:
                return None
        else:
            return example

    def process_report_examples(self, value, param_type=None):
        examples = []
        for example in value["provided"]:
            if example != "None":
                casted_example = self.process_cast_example(example, param_type)
                examples.append(casted_example) if casted_example is not None else None
        for example in value["generated"]:
            if example != "None":
                casted_example = self.process_cast_example(example, param_type)
                examples.append(casted_example) if casted_example is not None else None
        return examples

    def determine_max_number_examples(self, examples):
        max_val = 0
        for example_object in examples:
            example = example_object["examples"]
            if len(example) > max_val:
                max_val = len(example)
        return max_val

    def add_request_body_examples(self, constraint_list):
        example_constraints = {}
        for constraint in constraint_list:
            if constraint["request_body"]:
                for restriction in constraint["restrictions"]:
                    if restriction["restriction_name"] == "examples":
                        id = f"{constraint['path']}, {constraint['method']}"
                        if id in example_constraints:
                            example_constraints[id].append({"name": constraint["parameter"],
                                                            "examples": self.process_report_examples(
                                                                restriction["restriction_value"])})
                        else:
                            example_constraints[id] = [{"name": constraint["parameter"],
                                                        "examples": self.process_report_examples(
                                                            restriction["restriction_value"])}]

        for id, examples in example_constraints.items():
            path, method = id.split(", ")
            for application, schema in self.output_builder['paths'][path][method]["requestBody"]["content"].items():
                if application != 'description':
                    max_examples = self.determine_max_number_examples(examples)
                    example_collection = [[] for _ in range(max_examples)]
                    for example_object in examples:
                        for i in range(len(example_object["examples"])):
                            example_collection[i].append(
                                {"name": example_object["name"], "example": example_object["examples"][i]})
                    schema.setdefault("examples", {})
                    for i in range(len(example_collection)):
                        example_properties = {}
                        for specific_examples in example_collection[i]:
                            example_properties[specific_examples["name"]] = specific_examples["example"]
                        schema["examples"][f"example{i}"] = {"value": example_properties}

    def add_properties_with_report(self, constraint, parameter_properties, parameter_level, is_requestBody):
        special_properties = {"items", "x-dependencies", "examples", "properties"}
        check_consistency = {"collectionFormat", "format", "minimum", "maximum", "minLength", "maxLength", "minItems",
                             "maxItems", "minProperties", "maxProperties"}

        for restriction in constraint["restrictions"]:
            name = restriction["restriction_name"]
            value = restriction["restriction_value"]

            # Skip processing for 'max'
            if name == "max":
                continue  # Skip this iteration if 'max' is found

            if name == "minProperties" or name == "maxProperties":
                parameter_properties.setdefault(name, int(value))  # Ensure conversion to int

            if name == "type":
                if "type" not in parameter_properties:
                    parameter_properties["type"] = value

        for restriction in constraint["restrictions"]:
            if restriction["restriction_name"] == "type":
                continue

            name = restriction["restriction_name"]
            value = restriction["restriction_value"]

            if name not in special_properties and name not in check_consistency:
                parameter_properties.setdefault(name, value)

            elif name in check_consistency:
                if name == "collectionFormat" or name == "minItems" or name == "maxItems":
                    if parameter_properties["type"] == "array":
                        if name == "minItems" or name == "maxItems":
                            parameter_properties.setdefault(name, int(value))  # Ensure conversion to int
                        if name == "collectionFormat" and not is_requestBody:
                            # Move collectionFormat to 'items' schema
                            for parameter in parameter_level['parameters']:
                                if parameter["name"] == constraint["parameter"]:
                                    parameter['schema']['items'].setdefault("collectionFormat", value)  # Correct placement
                    elif name == "collectionFormat" and is_requestBody:
                        parameter_properties['items'].setdefault("collectionFormat", value)  # Correct placement

                elif name == "minimum":
                    if parameter_properties["type"] == "integer" or parameter_properties["type"] == "number":
                        parameter_properties.setdefault(name, int(value))

                elif name == "maximum":
                    if parameter_properties["type"] in ["integer", "number"]:
                        parameter_properties.setdefault(name, int(value))
                    else:
                        # Remove 'maximum' if type is not appropriate
                        parameter_properties.pop("maximum", None)

                elif name == "format" or name == "minLength":
                    if parameter_properties["type"] == "string":
                        if name == "format":
                            parameter_properties.setdefault(name, value)
                        else:
                            # Ensure minLength is an integer
                            parameter_properties.setdefault(name, int(value))
                elif name == "maxLength":
                    if parameter_properties["type"] == "string":
                        # Ensure maxLength is an integer
                        parameter_properties.setdefault(name, int(value))

            elif name in special_properties:
                if name == "x-dependencies":
                    parameter_level.setdefault(name, [])
                    for dependency in value:
                        parameter_level[name].extend(value)
                elif is_requestBody and "examples" in parameter_properties:
                    parameter_level.setdefault("examples", {})
                    for key, value in parameter_properties["examples"].items():
                        parameter_level["examples"][key] = value
                    del parameter_properties["examples"]
                elif name == "examples" and not is_requestBody:
                    param_type = {"is_int": False, "is_float": False, "is_bool": False}
                    for parameter in parameter_level['parameters']:
                        if parameter["name"] == constraint["parameter"]:
                            if parameter["schema"]["type"] == "integer":
                                param_type["is_int"] = True
                            elif parameter["schema"]["type"] == "number":
                                param_type["is_float"] = True
                            elif parameter["schema"]["type"] == "boolean":
                                param_type["is_bool"] = True

                    examples = self.process_report_examples(value, param_type)

                    for parameter in parameter_level['parameters']:
                        if parameter["name"] == constraint["parameter"]:
                            if "example" in parameter:
                                del parameter["example"]
                            parameter.setdefault("examples", {})
                            for i in range(len(examples)):
                                parameter['examples'][f"example{i}"] = {
                                    "value": examples[i]
                                }

                if name == "items":
                    parameter_properties.setdefault(name, {})
                    parameter_properties[name].setdefault("type", value)

    def change_specification_with_report(self, constraint_list):
        for constraint in constraint_list:
            if not constraint["request_body"]:
                parameter_level = self.output_builder['paths'][constraint["path"]][constraint["method"]]
                for parameter in parameter_level['parameters']:
                    if parameter["name"] == constraint["parameter"]:
                        self.add_properties_with_report(constraint, parameter["schema"], parameter_level, False)
            else:
                for application, schema in \
                        self.output_builder['paths'][constraint["path"]][constraint["method"]]["requestBody"][
                            "content"].items():
                    if application != 'description':
                        property_level = schema['schema']
                        if "properties" not in property_level:
                            self.add_properties_with_report(constraint, property_level, property_level, True)
                        else:
                            if "examples" in parameter_properties:
                                # Move the "examples" property to the content level
                                schema.setdefault("examples", {})
                                for key, value in parameter_properties["examples"].items():
                                    schema["examples"][key] = value
                                del parameter_properties["examples"]
                            parameter_properties = property_level['properties'][constraint["parameter"]]
                            self.add_properties_with_report(constraint, parameter_properties, property_level, True)

                self.add_request_body_examples(constraint_list)

    def add_parameter_description(self, constraint_list):
        for constraint in constraint_list:
            if not constraint["request_body"]:
                parameter_level = self.output_builder['paths'][constraint["path"]][constraint["method"]]
                for parameter in parameter_level['parameters']:
                    if parameter["name"] == constraint["parameter"]:
                        constraint["description"] = parameter.get("description", "None")
            else:
                for application, schema in \
                        self.output_builder['paths'][constraint["path"]][constraint["method"]]["requestBody"][
                            "content"].items():
                    if application != 'description':
                        property_level = schema['schema']
                        if "properties" not in property_level:
                            constraint["description"] = property_level.get("description", "None")
                        else:
                            parameter_properties = property_level['properties'][constraint["parameter"]]
                            constraint["description"] = parameter_properties.get("description", "None")

    def build_specification_with_report(self, file_path):
            print("Attempting generation at: " + file_path)
            with open(file_path, 'r') as json_file:
                report_values = json.load(json_file)

            constraint_list = self.find_report_constraints(report_values)

            # Only process the request body if it's not a GET request
            for constraint in constraint_list:
                if not constraint["request_body"] or (constraint["method"] != "GET" and constraint["request_body"]):
                    parameter_level = self.output_builder['paths'][constraint["path"]][constraint["method"]]
                    for parameter in parameter_level['parameters']:
                        if parameter["name"] == constraint["parameter"]:
                            self.add_properties_with_report(constraint, parameter["schema"], parameter_level, False)
                else:
                    for application, schema in \
                            self.output_builder['paths'][constraint["path"]][constraint["method"]]["requestBody"][
                                "content"].items():
                        if application != 'description':
                            property_level = schema['schema']
                            if "properties" not in property_level:
                                self.add_properties_with_report(constraint, property_level, property_level, True)
                            else:
                                if "examples" in parameter_properties:
                                    # Move the "examples" property to the content level
                                    schema.setdefault("examples", {})
                                    for key, value in parameter_properties["examples"].items():
                                        schema["examples"][key] = value
                                    del parameter_properties["examples"]
                                parameter_properties = property_level['properties'][constraint["parameter"]]
                                self.add_properties_with_report(constraint, parameter_properties, property_level, True)

                    self.add_request_body_examples(constraint_list)
    def build_specification(self):
        for path, method in self.paths:
            self.process_operation(path, method)
        self.create_output_file()

    def create_output_file(self):
        if not os.path.exists(os.path.dirname(self.output_path)):
            os.makedirs(os.path.dirname(self.output_path))
        if self.output_path.split(".")[-1] == 'yaml':
            with open(self.output_path, 'w') as yaml_file:
                yaml.dump(self.output_builder, yaml_file, default_flow_style=False, sort_keys=False)
        elif self.output_path.split(".")[-1] == 'json':
            with open(self.output_path, 'w') as json_file:
                json.dump(self.output_builder, json_file, indent=4, sort_keys=False)