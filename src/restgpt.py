from specification_builder import SpecificationBuilder
from report_builder import ReportBuilder
import os

def build_all_reports():
    original_files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    files = ["genome-nexus"]
    for file in files:
        print("Buidling specification for " + file)
        report_builder = ReportBuilder(f'specifications/openapi_yaml/{file}.yaml', f'{file}_results.json')
        report_builder.path_builder()
        report_builder.save_report_to_file()

def build_one_report(file_path, file_name):
    output_name = f"{file_name}_results.json"
    #report_builder = ReportBuilder(file_path, output_name)
    #report_builder.path_builder()
    #report_builder.save_report_to_file()
    spec_build = SpecificationBuilder(file_path, output_name)
    spec_build.build_specification()

def build_all_specs(file_type):
    original_files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    for file in files:
        print("Buidling specification for " + file)
        spec_builder = SpecificationBuilder(f'specifications/openapi_yaml/{file}.yaml', f'outputs/{file}_results.{file_type}')
        spec_builder.build_specification()

def build_one_spec(file_path, file_name):
    output_name = f"outputs/{file_name}_results.json"
    spec_build = SpecificationBuilder(file_path, output_name)
    spec_build.build_specification()

def build_all_specs_eval(file_type):
    try:
        files = os.listdir("specifications/inputs")
        for file in files:
            print("Buidling specification for " + file + ".")
            try:
                spec_builder = SpecificationBuilder(f'specifications/inputs/{file}', f'outputs/{file}_results.{file_type}')
                spec_builder.build_specification()
            except ImportError:
                print("The config file containing your API key does not exist.")
                return
            except KeyError:
                print("The API key used to access GPT-3.5 Turbo is invalid.")
                return
            except Exception:
                print(f"Failed to build specification for {file}.")
    except Exception:
        print("Failed to access input specifications.")


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
        spec_builder = SpecificationBuilder(f'specifications/openapi_yaml/{file}.yaml', f'outputs/openapi_yaml/{file}_results.yaml')
        spec_builder.build_specification_with_report(f"results/reports_update_512/{file}_results.json")

if __name__ == '__main__':
    file_type = input("Would you like to build the specifications in json(1) or yaml (2) format: ")
    if file_type == "1":
        file_type = "json"
    elif file_type == "2":
        file_type = "yaml"
    else:
        print("Invalid input. Please input either 1 or 2 according to the instructions.")
        exit()
    build_all_specs_eval(file_type) # uses the eval folder for the Docker containers
