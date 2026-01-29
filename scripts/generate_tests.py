import ast
import os
import sys
from google.genai import Client


def extract_functions(file_path):
    """Parse a Python file and extract function definitions."""

    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            args = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node) or ""
            func_source = ast.get_source_segment(source, node)

            functions.append({
                "name": func_name,
                "args": args,
                "docstring": docstring,
                "source": func_source
            })

    return functions


def generate_tests_for_function(func_info):
    """Use Gemini to generate pytest tests for a function."""

    client = Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = f"""
Generate pytest tests for this Python function.

Function name: {func_info['name']}
Arguments: {', '.join(func_info['args'])}
Docstring: {func_info['docstring']}

Source code:

{func_info['source']}

Requirements:
1. Generate 3–5 meaningful test cases
2. Include edge cases (empty inputs, None values, etc.)
3. Use descriptive test function names
4. Include assertions that actually test behavior
5. Do NOT generate placeholder tests like assert True

Return ONLY valid Python pytest code.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    test_code = response.text.strip()

    # Remove markdown fences if Gemini adds them
    test_code = test_code.replace("```python", "").replace("```", "")

    return test_code


def main():
    """Main function to generate tests for changed files."""

    changed_files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not changed_files:
        print("No Python files provided for test generation")
        return

    all_tests = []

    for file_path in changed_files:
        if not file_path.endswith(".py"):
            continue
        if file_path.startswith("tests/"):
            continue

        print(f"Analyzing: {file_path}")

        functions = extract_functions(file_path)

        for func in functions:
            if func["name"].startswith("_"):
                continue

            print(f"  Generating tests for: {func['name']}")

            tests = generate_tests_for_function(func)

            all_tests.append(
                f"# Tests for {func['name']} from {file_path}\n{tests}"
            )

    if all_tests:
        os.makedirs("tests", exist_ok=True)
        test_file = "tests/test_generated.py"

        with open(test_file, "w", encoding="utf-8") as f:
            f.write("import pytest\n\n")
            f.write("\n\n".join(all_tests))

        print(f"Generated tests written to: {test_file}")
    else:
        print("No functions found to generate tests for")


if __name__ == "__main__":
    main()
