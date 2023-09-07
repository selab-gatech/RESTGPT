from report_builder import ReportBuilder
import os
if __name__ == '__main__': 
    for file_name in os.listdir("specifications/openapi_yaml"):
        if file_name.endswith(".yaml"):
            print("buidling specification for " + file_name)
            report_builder = ReportBuilder(f'specifications/openapi_yaml/{file_name}', f'{file_name}_results.json')
            report_builder.path_builder()
            report_builder.save_report_to_file()
            report_builder.output_specifications()
    # report_builder = ReportBuilder('specifications/openapi_yaml/fdic.yaml', 'fdic_results.json')
    # report_builder.path_builder()
    # report_builder.save_report_to_file()
    #report_builder.output_specifications()