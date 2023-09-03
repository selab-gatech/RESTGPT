class parsed_spec_retrieval:
    def __init__(self, spec_parse): 
        if spec_parse is None: 
            raise Exception("Parsed OpenAPI specification is None")
        self.spec_parse = spec_parse
    def retrieve_specs(self, operation):
        if operation in self.spec_parse: 
            parameter_set = []
            for parameter in self.spec_parse[operation]: 
                parameter_set.append({k: v for k, v in parameter.items() if v is not None})
        return parameter_set 
    
             


        