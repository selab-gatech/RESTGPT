from report_builder import ReportBuilder
import os

def run_all_reports():
    for file_name in os.listdir("specifications/openapi_yaml"):
        if file_name.endswith(".yaml"):
            print("buidling specification for " + file_name)
            report_builder = ReportBuilder(f'specifications/openapi_yaml/{file_name}', f'{file_name}_results.json')
            report_builder.path_builder()
            report_builder.save_report_to_file()

def run_one_report(file_path, file_name):
    output_name = f"{file_name}_results.json"
    report_builder = ReportBuilder(file_path, output_name)
    report_builder.path_builder()
    report_builder.save_report_to_file()

if __name__ == '__main__':
    run_one_report("specifications/openapi_yaml/rest-countries.yaml", "rest-countries")