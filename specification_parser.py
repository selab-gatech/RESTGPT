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

def determine_parameter_object(parameter):
    return {
        "name": parameter.get("name"),
        "type": parameter.get("schema", {}).get('type'),
        "description": parameter.get("description"),
        "in": parameter.get("in"),
        "required": parameter.get("required"),
        "enum": parameter.get("schema", {}).get('enum'),
        "minimum": parameter.get("schema", {}).get("minimum"),
        "maximum": parameter.get("schema", {}).get("maximum"),
        "items": parameter.get("schema", {}).get("items", {}).get("type")
        if parameter.get("schema", {}).get("type") == "array" else None,
        "properties": parse_properties(parameter.get("schema", {}).get('properties', {}))
        if parameter.get("schema", {}).get("type") == "object" else None
    }

# Assume OpenAPI v3.0 files
def parse_parameters(file_path):
    try:
        parser = ResolvingParser(file_path, strict=False)
        spec_paths = parser.specification.get('paths', {}) # Determine all API paths while ignoring extraneous keys
        valid_http_methods = {'put', 'post', 'patch', 'get', 'delete'}
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
    result = parse_parameters("specifications/openapi_yaml/spotify.yaml")
    with open("test_files/results.json", 'w') as file:
        json.dump(result, file, indent=4)


