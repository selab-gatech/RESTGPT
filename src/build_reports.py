from report_builder import ReportBuilder
from specification_builder import SpecificationBuilder
import os

def run_all_reports():
    original_files = ["rest-countries", "omdb", "language-tool", "spotify", "youtube", "genome-nexus", "ohsome", "fdic", "ocvn"]
    files = ["genome-nexus"]
    for file in files:
        print("Buidling specification for " + file)
        report_builder = ReportBuilder(f'specifications/openapi_yaml/{file}.yaml', f'{file}_results.json')
        report_builder.path_builder()
        report_builder.save_report_to_file()

def run_one_report(file_path, file_name):
    output_name = f"{file_name}_results.json"
    #report_builder = ReportBuilder(file_path, output_name)
    #report_builder.path_builder()
    #report_builder.save_report_to_file()
    spec_build = SpecificationBuilder(file_path, output_name)
    spec_build.build_specification()


if __name__ == '__main__':
    run_one_report("specifications/openapi_yaml/youtube.yaml", "youtube")
    #run_all_reports()
