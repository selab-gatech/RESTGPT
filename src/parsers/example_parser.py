import yaml 
import re

class InputParser: 
    def __init__(self):
        pass
    def _split_values(self, llm_output):
        if llm_output == "None" or "+++" not in llm_output:
            return {
                "PROVIDED" : None, 
                "GENERATED" : None
            }
        split = llm_output.split("+++")
        extracted =  {
            "PROVIDED" : split[0].strip(), 
            "GENERATED" : split[1].strip()
        }
        extracted["PROVIDED"] = extracted["PROVIDED"].split("PROVIDED:")[1].strip().split(",") if extracted["PROVIDED"].split("PROVIDED:")[0].strip().lower() != "none" else None
        extracted["GENERATED"] = extracted["GENERATED"].split("GENERATED:")[1].strip().split(",") if extracted["GENERATED"].split("GENERATED:")[1].strip().lower() != "none" else None
        return extracted
    def parse_enum(self, llm_output):
        extracted_values = self._split_values(llm_output)
        enum = []
        for key in extracted_values.keys():
            if extracted_values[key] is not None:
                    enum.extend(extracted_values[key])
        return enum, enum[0] if enum else None
    def parse_examples(self, llm_output, is_requestBody=False, parameter_name=None): 
        extracted_values = self._split_values(llm_output)
        provided_examples = extracted_values["PROVIDED"]
        generated_examples = extracted_values["GENERATED"]
        if not is_requestBody: 
            if len(provided_examples) + len(generated_examples) == 1: 
                return {
                    "example": provided_examples[0] if provided_examples else generated_examples[0] 
                }
            else: 
                example_dict = {"examples" : {}}
                provided_base =  "PROVIDED"
                generated_base = "GENERATED"
                for i in range(len(provided_examples)):
                    example_dict["examples"][f"{provided_base}_{i}"] = {}
                    example_dict["examples"][f"{provided_base}_{i}"]["value"] = provided_examples[i]
                for i in range(len(generated_examples)):
                    example_dict["examples"][f"{generated_base}_{i}"] = {}
                    example_dict["examples"][f"{generated_base}_{i}"]["value"] = generated_examples[i]
                return example_dict
        else:
            example_dict = {"examples" : {}}
            provided_base =  "PROVIDED_" + parameter_name 
            generated_base = "GENERATED_" + parameter_name
            for i in range(len(provided_examples)):
                example_dict["examples"][f"{provided_base}_{i}"] = {}
                example_dict["examples"][f"{provided_base}_{i}"]["value"] = str({parameter_name: provided_examples[i]})
            for i in range(len(generated_examples)):
                example_dict["examples"][f"{generated_base}_{i}"] = {}
                example_dict["examples"][f"{generated_base}_{i}"]["value"] = str({parameter_name: generated_examples[i]})
            return example_dict

            

        

        

        

    