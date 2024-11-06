# RESTGPT

RESTGPT is an approach to automated API testing that leverages Large Language Models (LLMs) to maximize relevant test cases. The program intakes OpenAPI Specifications and, using gpt-4o-mini pre-trained LLM to create machine-readable rules from human-readable fields, produces enhanced OpenAPI Specification outputs for automated API testing software.

## Use of Software

The RESTGPT Github currently contains OpenAPI Specifications from 9 different wide-spread commercial APIs: **FDIC, Genome-Nexus, Language-Tool, OCVN, Ohsome, OMDB, Rest-Countries, Spotify,** and **Youtube**. To access these files, navigate to `src/specifications/openapi_yaml` or `src/specifications/openapi_json`.

After downloading the Github repository, one must simply do three things to generate results for either the 9 pre-added OpenAPI Specifications or their own select inputs:
1. Download the packages specified in the `requirements.txt` file.
2. Create a `.env` file in the root directory with an [**OpenAI API Key**](https://platform.openai.com/account/api-keys) as the sole piece of content.
> **Note:**
> Running the program can cost over $10 in OpenAI token costs. The cost varies on input quantity.
3. Alter the `configurations.py` file's RUN_MODE variable to suit the use case.

RESTGPT offeres three run modes: "predefined", "custom", and "docker". The "predefined" mode will run the program with the 9 pre-added OpenAPI Specifications, the "custom" mode will run the program with user-defined OpenAPI Specifications, and the "docker" mode will run the program with Docker configurations using custom specifications.

> **Note:**
> The `custom` and `docker` run modes both require a `src/specification/inputs` folder with the desired input OpenAPI Specifications. Refer to the **Customization** section for more details. The `predefined` mode will work with the 9 pre-added OpenAPI Specifications and was used within the RESTGPT paper.

When using the _predefined_ or _custom_ run modes, execute the following command in the root directory to run RESTGPT:
```
python3 restgpt.py <FILE_TYPE>
```
> **Note:**
> Fill in the "<FILE_TYPE>" parameter with either "json" or "yaml" (without quotes) to specify the desired output type of the OpenAPI Specifications.

Refer to the **Use of Docker Container** section for executing the program with Docker configurations.

Results will be generated in the `src/outputs` directory, with a different file representing the enhanced report for each of their corresponding OpenAPI Specifications. 

## Use of Docker Container

The RESTGPT repository currently contains a pre-made Dockerfile for consistency in replicability. After downloading the Github repository with the Dockerfile, one must follow the following short steps to create the Docker container:
1. On the local system, create the `src/specifications/inputs` folder with the desired input OpenAPI Specifications.
2. Create a `.env` file in the root directory with an [**OpenAI API Key**](https://platform.openai.com/account/api-keys) as the sole piece of content.
> **Note:**
> Running the program can cost over $10 in OpenAI token costs. The cost varies on input quantity.
3. Build the Docker image with the following commands executed sequentially in the root directory:
```
docker build -t restgpt .
docker run -e FILE_TYPE=<your_value> restgpt
```

> **Note:**
> Fill in the "<your_value>" parameter with either "json" or "yaml" (without quotes) to specify the desired output type of the OpenAPI Specifications. Otherwise, the execution will default to json outputs.

Results will be generated within the `app/src/outputs` folder of the Docker container. Any failure to comply with the instructions, such as not creating and supplying the inputs folder or not creating the `config.py` folder, may result in improper completion on the `docker run` stage.

## LLM Prompt-Response CSV

To provide further context for the results of RESTGPT, the repository contains a list of CSV files that show the prompts and responses sent and received to the LLM when generating the enhanced specifications. The `src/csv` folder contains the corresponding CSVs for the 9 pre-added OpenAPI Specifications. The CSVs contain the **temperature**, **token limit**, **parameter name**, **prompt**, and **response** for each LLM query.

## Customization

**Changing LLMs:** RESTGPT uses gpt-4o-mini as its Large Language Model, however the program can support any of OpenAI's available LLMs. To switch the LLM, navigate to `src/restgpt.py` and find the following line:
```
llm = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=256, openai_api_key = API_KEY, temperature=0.2, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
```
Swap the "model_name" string for any of the OpenAI model codes.

**Changing Specifications:** The program and the results come alongside 9 OpenAPI Specifications for Proof of Concepts. However, if one would like to use different specifications, navigate to `src/specifications/openapi_yaml` and add the desired OpenAPI Specification file in **yaml** format.

## Results

The results for the [NLPtoREST vs. RESTGPT comparison](https://docs.google.com/spreadsheets/d/1_8WJ6GkmMhOOTBmXf3d9vMPF5r7FrE34A51fHcyOQPA/edit?usp=sharing) evaluate the validity of the rules extracted from the human-readable description fields. Firstly, a "ground truth" table is created through multiple professionals' (graduate students) analysis of the parameter descriptions. Then, both software outputs are analyzed to determine whether their OpenAPI Specification keyword values match the ground truth table. Results are provided as **true positives (TP)** if the correct restriction and keyword was output, **false positives (FP)** if an incorrect restriction and keyword was output, and **false negative** if no restriction or keyword was output when one was expected.

The results for the [ARTE vs. RESTGPT comparison](https://docs.google.com/spreadsheets/d/1NLgmgkgMhnl31Z1_Z3j6-9aGUVhPEo67h6vkMKZnfFI/edit?usp=sharing) evaluate **semantic** and **syntactic** validity for generated examples from the respective softwares. Syntactic validity was determined through analyzing whether the examples provided matched limitations on the input fields, such as data types, from the human-readable description. Semantic validity was determined through analyzing whether the examples matched the meaning of the human-readable description, such as a limitation to only ISO-3166 country codes. In all cases, **syntactic validity** indicated a successful example.
