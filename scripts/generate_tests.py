import ast
import os
import sys
import time
from google import genai
from google.genai import errors

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

# Define a function that generates tests for multiple functions in one API call
def generate_all_tests(all_functions, max_retries=5, initial_delay=60):
    """Use Gemini to generate pytest tests for all functions in one call."""

    # Create a Gemini client using your API key from environment variables
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # Build a combined prompt with all functions
    functions_text = ""
    for file_path, func_info in all_functions:
        functions_text += f"""
--- Function from {file_path} ---
Function name: {func_info['name']}
Arguments: {', '.join(func_info['args'])}
Docstring: {func_info['docstring']}

Source code:
{func_info['source']}

"""

    prompt = f"""Generate pytest tests for these Python functions.

{functions_text}

Requirements:
1. Generate 3-5 meaningful test cases per function
2. Include edge cases (empty inputs, None values, etc.)
3. Use descriptive test function names
4. Include assertions that actually test behavior
5. Do NOT generate placeholder tests like `assert True`
6. Add necessary imports at the top (like 'from app import add, multiply' etc.)

Return ONLY the Python test code, no explanations or markdown code blocks.
"""

    # Retry loop with exponential backoff for rate limits
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            # Send the prompt to the model and get a response
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            # Return just the text from the response
            return response.text
        except errors.ClientError as e:
            if '429' in str(e) or 'RESOURCE_EXHAUSTED' in str(e):
                if attempt < max_retries - 1:
                    print(f"  Rate limited. Waiting {delay}s before retry...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    raise
            else:
                raise

def main():
    """Main function to generate tests for changed files."""

    # Get list of changed Python files from command-line arguments
    changed_files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not changed_files:
        print("No Python files provided for test generation")
        return

    # Collect all functions first
    all_functions = []

    for file_path in changed_files:
        # Skip non-Python files
        if not file_path.endswith('.py'):
            continue
        # Skip test files
        if file_path.startswith('tests/'):
            continue

        print(f"Analyzing: {file_path}")
        functions = extract_functions(file_path)

        for func in functions:
            # Skip private functions (those starting with _)
            if func['name'].startswith('_'):
                continue

            print(f"  Found function: {func['name']}")
            all_functions.append((file_path, func))

    if all_functions:
        # Generate tests for all functions in one API call
        print(f"\nGenerating tests for {len(all_functions)} functions...")
        tests = generate_all_tests(all_functions)

        # Create tests directory if it doesn't exist
        os.makedirs('tests', exist_ok=True)
        test_file = 'tests/test_generated.py'

        with open(test_file, 'w') as f:
            f.write(tests)

        print(f"Generated tests written to: {test_file}")
    else:
        print("No functions found to generate tests for")


# Only run this code when the script is executed directly
if __name__ == "__main__":
    main()
