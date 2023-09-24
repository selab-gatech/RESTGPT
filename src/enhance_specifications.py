from specification_builder import SpecificationBuilder
import os

def run_all_reports():
    original_files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    for file in files:
        print("Buidling specification for " + file)
        spec_builder = SpecificationBuilder(f'specifications/openapi_yaml/{file}.yaml', f'outputs/{file}_results.json')
        spec_builder.build_specification()

def run_one_report(file_path, file_name):
    output_name = f"outputs/{file_name}_results.json"
    spec_build = SpecificationBuilder(file_path, output_name)
    spec_build.build_specification()


if __name__ == '__main__':
    #run_one_report("specifications/openapi_yaml/omdb.yaml", "omdb")
    run_all_reports()
