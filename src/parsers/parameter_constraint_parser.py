import yaml

class ParameterConstraintParser:
    def __init__(self):
        pass
    def dictionary_output(self, min_restriction, max_restriction):
        return {min_restriction[0]: min_restriction[1], max_restriction[0]: max_restriction[1]}

    def yaml_output(self, min_restriction, max_restriction):
        return yaml.dump(self.dictionary_output(min_restriction, max_restriction))

    def parse(self, restriction_string, output_type=None):
        if restriction_string is None or restriction_string.strip() == "None":
            return
        restrictions = restriction_string.split(", ")
        min_restriction = restrictions[0].split(" ")
        max_restriction = restrictions[1].split(" ")
        return self.yaml_output(min_restriction, max_restriction) if output_type == "yaml" else self.dictionary_output(min_restriction, max_restriction)
    