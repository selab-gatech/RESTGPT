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
        parameter_data[method_key].append(determine_parameter_object(parameter))
    if 'requestBody' in method_values:
        request_body  = {}
        request_body["specifier"] = "requestBody"
        request_body["description"] = method_values.get("requestBody").get('description', '')
        parameters = []
        required_parameters = []
        for encoding in method_values.get("requestBody").get("content").keys():
            request_body_schema = method_values.get("requestBody").get("content").get(encoding).get("schema")
            parameters.append(request_body_schema.get("properties"))
            if "required" in request_body_schema.keys(): 
                required_parameters.extend(request_body_schema.get("required"))
        required_parameters = set(required_parameters)
        constructed_parameters = []
        for parameter in parameters: 
            for name in parameter.keys():
                if name in required_parameters:
                    parameter[name]["required"] = True
                else:
                    parameter[name]["required"] = False
                constructed_parameters.append({
                    "name" : name, 
                    "type" : parameter[name].get("type"), 
                    "description" : parameter[name].get("description"),
                    "in" : "body",
                    "required" : parameter[name].get("required"),
                    "enum" : parameter[name].get("enum"),
                    "minimum" : parameter[name].get("minimum"),
                    "maximum" : parameter[name].get("maximum"),
                    "items" : parameter[name].get("items", {}).get("type"),
                    "format" : parameter[name].get("format")
                    if parameter[name].get("type") == "array" else None,
                    "properties" : parse_properties(parameter[name].get("items", {}).get('properties', {})) if parameter.get("type") == "object" else None,
                })
        request_body["request_parameters"] = constructed_parameters
        parameter_data[method_key].append(request_body)
    

def determine_parameter_object(parameter):
    schema = parameter.get("schema", {})
    return {
        "name": parameter.get("name"),
        "type": schema.get('type'),
        "description": parameter.get("description"),
        "in": parameter.get("in"),
        "required": parameter.get("required"),
        "enum": schema.get('enum'),
        "minimum": schema.get("minimum"),
        "maximum": schema.get("maximum"),
        "items": schema.get("items", {}).get("type"),
        "format": schema.get("format")
        if parameter.get("schema", {}).get("type") == "array" else None,
        "properties": parse_properties(parameter.get("schema", {}).get('properties', {}))
        if parameter.get("schema", {}).get("type") == "object" else None,
        "specifier" : "parameter"
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
    result = parse_parameters("../specifications/openapi_yaml/spotify.yaml")
    with open("test_specification.json", 'w') as file:
        json.dump(result, file, indent=4)


