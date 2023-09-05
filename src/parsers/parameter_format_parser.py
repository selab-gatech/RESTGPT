import yaml

class ParameterFormatParser:
    def __init__(self):
        pass

    def dictionary_output(self, type_value, items_value, format_value):
        return {type_value[0]: type_value[1], items_value[0]: items_value[1], format_value[0]: format_value[1]}

    def yaml_output(self, type_value, items_value, format_value):
        return yaml.dump(self.dictionary_output(type_value, items_value, format_value))

    def parse(self, format_string, output_type):
        if format_string is None:
            pass
        values = format_string.split(", ")
        type_value = values[0].split(" ")
        items_value = values[1].split(" ") # REMEMBER TO CHECK TYPE VALUE WHEN ADDING ITEM IN OVERALL PARSER
        format_value = values[2].split(" ")
        return self.yaml_output(type_value, items_value, format_value) if output_type == "yaml" else \
            self.dictionary_output(type_value, items_value, format_value)

if __name__ == "__main__":
    parser = ParameterFormatParser()
    print(parser.parse("type string, items None, format url", "dict"))

