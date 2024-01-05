import argparse
from llm import run_llm_chain

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the RESTGPT tool.')
    parser.add_argument('--file_path', type=str, help='The path to the OpenAPI specification file.', required=True)
    parser.add_argument('--method_path', type=str, help='The path to the method in the OpenAPI specification file.', required=True)
    parser.add_argument('--method_type', type=str, help='The HTTP method type for the method in the OpenAPI specification file.', required=True)
    args = parser.parse_args()

    file_path = args.file_path
    method_path = args.method_path
    method_type = args.method_type

    print(run_llm_chain(file_path, method_path, method_type))
    
    