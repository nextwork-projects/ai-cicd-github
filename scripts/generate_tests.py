import ast
from google import genai
import sys
import os


def extract_functions(file_path):
    #Read the source code
    with open(file_path, "r") as f:
        source = f.read()

    #parse it into a tree
    tree = ast.parse(source)

    #Walk through the tree to find node
    function = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_info = {
                "name": node.name,
                "arguments": [ag.arg for arg in node args.args],
                "docstring": ast.get_docstring(node),
                "source": ast.get_source_segment(source, node),
            }
            functions.append(func_info)
        return function


def generate_tests_for_function(func_info):
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    prompt = f"""
    You are an expert Python developer. Generate 3 - 5 meaningful pytest test cases for the following function.

    Function name: {func_info['name']}
    Arguments: {func_info['arguments']}
    Docstring: {func_info['docstring']}
    Source: {func_info['source']}

    Rules:
    - Do not write placeholder tests like assert True or assert False
    - Each tests must actually call the function with real arguments.
    - Test edge cases like empty input, negative numbers, or none where relevant
    - Each testfunction must have a descriptive name explaining what it tests
    - Only return the code, no explanations
    """

   response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
   )  

   return response.txt



def main():
    file_paths = sys.argv[1:]

    all_tests = []

    for file_path in file_paths:
        if not file_path.endswith(".py"):
            print(f"Skipping {file_path} — not a Python file")
            continue

        if "test" in file_path:
            print(f"Skipping {file_path} — looks like a test file")
            continue

        functions = extract_functions(file_path)

        for func in functions:
            if func["name"].startswith("_"):
                print(f"Skipping private function: {func['name']}")
                continue

            print(f"Generating tests for {func['name']}...")
            tests = generate_tests_for_function(func)
            all_tests.append(tests)

    os.mkdir("tests", exist_ok=True)

    with open("tests/test_generated.py", "w") as f:
        f.write("\n\n".join(all_tests))

    print("Done! Tests written to tests/test_generated.py")


if __name__ == '__main__':
    main()
