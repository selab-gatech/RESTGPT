import yaml

class ParameterFormatParser:
    def __init__(self):
        pass

    def dictionary_output(self, type_value, items_value, format_value, collection_format):
        return {type_value[0]: type_value[1], items_value[0]: items_value[1], format_value[0]: format_value[1], collection_format[0]: collection_format[1]}

    def yaml_output(self, type_value, items_value, format_value, collection_format):
        return yaml.dump(self.dictionary_output(type_value, items_value, format_value, collection_format))

    def parse(self, format_string, output_type=None):
        if format_string is None or format_string.strip() == "None":
            return
        values = format_string.split(", ")
        type_value = values[0].split(" ")
        items_value = values[1].split(" ") # REMEMBER TO CHECK TYPE VALUE WHEN ADDING ITEM IN OVERALL PARSER
        format_value = values[2].split(" ")
        collection_format = values[3].split(" ")
        return self.yaml_output(type_value, items_value, format_value, collection_format) if output_type == "yaml" else \
            self.dictionary_output(type_value, items_value, format_value, collection_format)

if __name__ == "__main__":
    parser = ParameterFormatParser()
    print(parser.parse("type string, items None, format url", "dict"))

