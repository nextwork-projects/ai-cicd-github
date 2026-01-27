import ast
import os
import sys
from google import genai

# Define a function that takes a file path and extracts function info
def extract_functions(file_path):
    """Parse a Python file and extract function definitions."""

    # Open the file and read its contents into a string
    with open(file_path, 'r') as f:
        source = f.read()

    # Parse the source code into an AST tree
    tree = ast.parse(source)
    functions = []

    # Walk through every node in the AST
    for node in ast.walk(tree):
        # Check if this node is a function definition
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            args = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node) or ""
            func_source = ast.get_source_segment(source, node)

            functions.append({
                'name': func_name,
                'args': args,
                'docstring': docstring,
                'source': func_source
            })

    return functions

# Define a function that generates tests for a given function's info
def generate_function_tests(func_info):
    """Use Gemini to generate pytest tests for a function."""

    # Create a Gemini client using your API key from environment variables
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # Write a multi-line prompt that includes the function details
    prompt = f"""Generate pytest tests for this Python function.

Function name: {func_info['name']}
Arguments: {', '.join(func_info['args'])}
Docstring: {func_info['docstring']}

Source code:

{func_info['source']}

Requirements:
1. Generate 3-5 meaningful test cases
2. Include edge cases (empty inputs, None values, etc.)
3. Use descriptive test function names
4. Include assertions that actually test behavior
5. Do NOT generate placeholder tests like `assert True`

Return ONLY the Python test code, no explanations.
"""

    # Send the prompt to the model and get a response
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    # Return just the text from the response
    return response.text

def main():
    """Main function to generate tests for changed files."""

    # Get list of changed Python files from command-line arguments
    changed_files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not changed_files:
        print("No Python files provided for test generation")
        return

    all_tests = []

    for file_path in changed_files:
        # Skip non-Python files
        if not file_path.endswith('.py'):
            continue
        # Skip test files
        if file_path.startswith('/tests'):
            continue

        print(f"Analyzing: {file_path}")
        functions = extract_functions(file_path)

        for func in functions:
            # Skip private functions (those starting with _)
            if func['name'].startswith('_'):
                continue

            print(f"  Generating tests for: {func['name']}")
            tests = generate_function_tests(func)
            all_tests.append(f"# Tests for {func['name']} from {file_path}\n{tests}")

    if all_tests:
        # Create tests directory if it doesn't exist
        os.makedirs('tests', exist_ok=True)
        test_file = 'tests/test_generated.py'

        with open(test_file, 'w') as f:
            f.write("import pytest\n\n")
            f.write("\n\n".join(all_tests))

        print(f"Generated tests written to: {test_file}")
    else:
        print("No functions found to generate tests for")


# Only run this code when the script is executed directly
if __name__ == "__main__":
    main()
