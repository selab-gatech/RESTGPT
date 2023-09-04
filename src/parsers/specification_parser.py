from prance import ResolvingParser
import json

def parse_properties(properties, data = {}, layer = 2):
    for property_name, property_value in properties.items():
        data[property_name] = {
            "type": property_value.get("type"), # Verify after testing that they object items don't have schemas
            "descrption": property_value.get("description"),
            "items": property_value.get("items", {}).get("type") if property_value.get("type") == "array" else None,
            "properties": parse_properties(property_value.get("items", {}).get("properties", {}), {}, layer + 2)
            if property_value.get("items", {}).get("type") == "object" else None
        }
    return data

def process_method_values(method_key, method_values, parameter_data):
    parameter_data[method_key] = []
    for parameter in method_values.get('parameters', {}):
        parameter_data[method_key].append(
            determine_parameter_object(
                parameter.get("schema", {}),
                parameter.get("name"),
                parameter.get("description"),
                parameter.get("in"),
                parameter.get("required"),
                "parameter"
            )
        )
    if 'requestBody' in method_values:
        request_body  = {"specifier": "requestBody",
                         "description": method_values.get("requestBody").get('description', '')}
        parameters = []
        required_parameters = []
        for encoding, encoding_values in method_values.get("requestBody", {}).get("content", {}).items():
            request_body_schema = encoding_values.get("schema", {})
            parameters.append({"properties": request_body_schema.get("properties"), "encoding": encoding})
            if "required" in request_body_schema.keys():
                required_parameters.extend(request_body_schema.get("required"))
        required_parameters = set(required_parameters)
        for parameter in parameters:
            properties = parameter.get("properties", {})
            encoding = parameter.get("encoding")
            if properties is None: # CURRENTLY NOT HANDLING $ref
                continue
            for name in properties.keys():
                if name in required_parameters:
                    properties[name]["required"] = True
                else:
                    properties[name]["required"] = False
                parameter_data[method_key].append(
                    determine_parameter_object(
                        value=properties[name],
                        name=name,
                        description=properties[name].get("description"),
                        in_value="requestBody",
                        required=properties[name].get("required"),
                        specifier="requestBody",
                        encoding=encoding
                    )
                )

def determine_parameter_object(value, name, description, in_value, required, specifier, encoding=None):
    return {
        "name": name,
        "type": value.get('type'),
        "description": description,
        "in": in_value,
        "required": required,
        "enum": value.get('enum'),
        "minimum": value.get("minimum"),
        "maximum": value.get("maximum"),
        "items": value.get("items", {}).get("type"),
        "format": value.get("format")
        if value.get("type") == "array" else None,
        "properties": parse_properties(value.get('properties', {}))
        if value.get("type") == "object" else None,
        "specifier" : specifier,
        "encoding" : encoding
    }

# Assume OpenAPI v3.0 files
def parse_parameters(file_path):
    try:
        parser = ResolvingParser(file_path, strict=False)
        spec_paths = parser.specification.get('paths', {}) # Determine all API paths while ignoring extraneous keys
        valid_http_methods = {'put', 'post', 'patch', 'get', 'delete', 'options', 'head', 'patch', 'trace'}
        parameter_data = {}

        for path, path_values in spec_paths.items():
            for method_type, method_values in path_values.items(): # Determine HTTP method
                if method_type in valid_http_methods:
                    method_key = f"{path} {method_type}"
                    process_method_values(method_key, method_values, parameter_data)

        return parameter_data
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    # Testing
    result = parse_parameters("../specifications/openapi_yaml/ocvn.yaml")
    with open("../../test_files/test_specification.json", 'w') as file:
        json.dump(result, file, indent=4)


