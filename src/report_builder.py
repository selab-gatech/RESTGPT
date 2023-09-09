from restgpt import run_llm_chain
from parsers.ipd_parser import InterDependencyParser
from prance import ResolvingParser, BaseParser
from parsers.parameter_constraint_parser import ParameterConstraintParser
from parsers.example_parser import ExampleParser
from parsers.parameter_format_parser import ParameterFormatParser
from parsers.specification_parser import parse_parameters
import json
import os
import hashlib
from tqdm import tqdm

class ReportBuilder: 
    def __init__(self, read_path, output_path): 
        self.ipd_parser = InterDependencyParser()
        self.example_parser = ExampleParser()
        self.parameter_constraint_parser = ParameterConstraintParser()
        self.parameter_format_parser = ParameterFormatParser()
        self.output_builder = ResolvingParser(read_path, strict=False).specification #reads in the specification as a dictionary
        self.read_path = read_path
        self.output_path = output_path
        valid_http_methods = {'put', 'post', 'patch', 'get', 'delete', 'options', 'head', 'patch', 'trace'}
        self.paths = []
        for path, path_values in self.output_builder.get('paths', {}).items():
            for method_type, method_values in path_values.items(): # Determine HTTP method
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
    
    def _convert_key(self, path):
        return f'{path[0]} {path[1]}'
        

    def _add_parameter_constraint(self, build_parameter, parameter_constriant): 
        if parameter_constriant is None:
            return
        for constraint_key, constraint in parameter_constriant.items(): 
            build_parameter[constraint_key] = constraint
    def _add_ipd_constraint(self, build_parameter, ipd_constraint):
        if ipd_constraint is None:
            return
        for constraint in ipd_constraint:
            build_parameter["x-dependencies"] = constraint
    def _add_example_values(self, build_parameter, model_examples):
        if model_examples is None: 
            return
        example_key = "examples"
        build_parameter[example_key] = {} 
        build_parameter[example_key]["provided"] = []
        build_parameter[example_key]["generated"] = []
        for key in model_examples.keys():
            for id, example in model_examples[key].items():
                if id.split("_")[0] == "PROVIDED": 
                    build_parameter[example_key]["provided"].append(example["value"])
                else: 
                    build_parameter[example_key]["generated"].append(example["value"])
    def _add_parameter_type_values(self, build_parameter, parameter_types):
        if parameter_types is None: 
            return None
        for type_key, extracted_type in parameter_types.items(): 
            if type_key == "items":
                if parameter_types["type"] == "array":
                    build_parameter[type_key] = extracted_type
            else:
                build_parameter[type_key] = extracted_type
    
    def _save_run_ai(self,read_path, route, method):
        check = hashlib.md5(open('restgpt.py', 'rb').read()).hexdigest()
        gpt_modified = True
        if os.path.isfile(".last_modified"):
            with open(".last_modified", "r") as f:
                last_modified = f.read().splitlines()
                last_modified = set(last_modified)
                if check in last_modified:
                    gpt_modified = False
        else: 
            with open(".last_modified", "w") as f:
                f.write(check)
        with open("llm_output.json", "w") as f:
            f.write("{}")
        with open("llm_output.json", "r+") as f:
            data = json.load(f)
            if gpt_modified or data.get(route + " " + method) is None:
                completed = run_llm_chain(read_path, route, method)
                data[route + " " + method] = completed
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return data[route + " " + method]
            else: 
                return data[route + " " + method]
        
    # def _run_one_iter_path_builder(self):
    #     path = self.paths[1]
    #     route = path[0]
    #     method = path[1]
    #     request_body_id = "request-body"
    #     spec = {}
    #     spec[route] = {method : {}}
    #     operation_constraints = self._save_run_ai(self.read_path, route, method)
    #     for parameter in operation_constraints: 
    #         parameter_spec = {}
    #         self._add_parameter_constraint(parameter_spec, self.parameter_constraint_parser.parse(parameter["parameter_constraints"]))
    #         self._add_ipd_constraint(parameter_spec, self.ipd_parser.parse_parameter(parameter["operational_constraints"]))
    #         self._add_example_values(parameter_spec, self.example_parser.parse_examples(parameter["parameter_examples"], is_requestBody=False, parameter_name=parameter["name"]))
    #         self._add_parameter_type_values(parameter_spec, self.parameter_format_parser.parse(parameter["parameter_formats"]))
    #         if parameter["name"] in self.method_parameter_set[self._convert_key(path)]:
    #             spec[route][method][parameter["name"]] = parameter_spec
    #         else: 
    #             if request_body_id in spec[route][method].keys():
    #                 spec[route][method][request_body_id][parameter["name"]] = parameter_spec
    #             else: 
    #                 spec[route][method][request_body_id] = {} 
    #                 spec[route][method][request_body_id][parameter["name"]] = parameter_spec
    #     return spec
    
    def path_builder(self): 
        spec = {}
        for path in self.paths:
            #print(path)
            route = path[0]
            method = path[1]
            request_body_id = "request-body"
            if route not in spec.keys():
                spec[route] = {method : {}}
            else:
                spec[route][method] = {}
            operation_constraints = self._save_run_ai(self.read_path, route, method)
            for parameter in operation_constraints: 
                parameter_spec = {}
                self._add_parameter_constraint(parameter_spec, self.parameter_constraint_parser.parse(parameter["parameter_constraints"]))
                self._add_ipd_constraint(parameter_spec, self.ipd_parser.parse_parameter(parameter["operational_constraints"]))
                self._add_example_values(parameter_spec, self.example_parser.parse_examples(parameter["parameter_examples"], is_requestBody=False, parameter_name=parameter["name"]))
                self._add_parameter_type_values(parameter_spec, self.parameter_format_parser.parse(parameter["parameter_formats"]))
                if parameter["name"] in self.method_parameter_set[self._convert_key(path)]:
                    spec[route][method][parameter["name"]] = parameter_spec
                else: 
                    if request_body_id in spec[route][method].keys():
                        spec[route][method][request_body_id][parameter["name"]] = parameter_spec
                    else: 
                        spec[route][method][request_body_id] = {} 
                        spec[route][method][request_body_id][parameter["name"]] = parameter_spec
        self.report = spec
    
    def save_report_to_file(self):
        if self.output_path.split(".")[-1] != "json":
            raise Exception("must output to json file")
        #TODO write self.report to filename json
        write_dump = json.dumps(self.report, indent=4)
        with open(self.output_path, "w") as f:
            f.write(write_dump)