from specification_builder import SpecificationBuilder
import os

def build_all_specs():
    original_files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    for file in files:
        print("Buidling specification for " + file)
        spec_builder = SpecificationBuilder(f'specifications/openapi_yaml/{file}.yaml', f'outputs/{file}_results.json')
        spec_builder.build_specification()

def build_one_spec(file_path, file_name):
    output_name = f"outputs/{file_name}_results.json"
    spec_build = SpecificationBuilder(file_path, output_name)
    spec_build.build_specification()

def build_one_spec_with_report(file_path, file_name):
    # language tool to test requestBody
    # omdb to test general

    output_path = f"outputs/{file_name}_results.json"
    spec_build = SpecificationBuilder(file_path, output_path)
    spec_build.build_specification_with_report(f"results/reports_update_512/{file_name}_results.json")

def build_all_specs_with_reports(): # run this for RESTGPT paper enhanced specification generation
    original_files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic",
                      "ocvn"]
    files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    for file in files:
        print("Building enhanced specifictaion for " + file)
        spec_builder = SpecificationBuilder(f'specifications/openapi_yaml/{file}.yaml', f'outputs/{file}_results.json')
        spec_builder.build_specification_with_report(f"results/reports_update_512/{file}_results.json")

if __name__ == '__main__':
    #build_one_spec_with_report("specifications/openapi_yaml/language-tool.yaml", "language-tool")
    #build_one_spec_with_report("specifications/openapi_yaml/omdb.yaml", "omdb")
    build_all_specs_with_reports()
