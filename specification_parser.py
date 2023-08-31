from prance import ResolvingParser


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

def determineParameterObject(parameter):
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
    parser = ResolvingParser(file_path)
    spec_paths = parser.specification.get('paths', {}) # Determine all API paths while ignoring extraneous keys
    valid_http_methods = {'put', 'post', 'patch', 'get', 'delete'}
    parameter_data = {}

    for path, path_values in spec_paths.items():
        for method_type, method_values in path_values.items(): # Determine HTTP method
            if method_type in valid_http_methods:
                method_key = f"{method_type} {path}"
                parameter_data[method_key] = []
                for parameter in method_values.get('parameters', {}):
                    parameter_data[method_key].append(determineParameterObject(parameter))

if __name__ == "__main__":
    # Testing
    parse_parameters("specifications/openapi_yaml/spotify.yaml")


