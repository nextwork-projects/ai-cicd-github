import os
import json
import time
from pathlib import Path
from google import genai

# Create a Gemini client, passing in the API key from environment variables
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_python_files(repo_path: str) -> list[str]:
    """Find all Python files in the repository."""
    python_files = []

    for path in Path(repo_path).rglob("*.py"):
        # Skip virtual environments and common directories to ignore
        if any(part in path.parts for part in ["venv", ".venv", "node_modules", "__pycache__", ".git"]):
            continue
        python_files.append(str(path))


    return python_files

def read_file_content(file_path: str) -> str:
    """Read and return the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def analyze_code(code_content: str, file_path: str) -> dict:
    """Send code to Gemini for dead code analysis."""
    prompt = f"""Analyze the following Python code and identify any dead code.

Look for:
1. Unused functions (defined but never called within this file)
2. Dead imports (imported but never used)
3. Unreachable code (code after return statements, etc.)

File: {file_path}

Code:

{code_content}


Respond in JSON format with this structure:
{{
    "findings": [
        {{
            "type": "unused_function" | "dead_import" | "unreachable_code",
            "name": "name of the function/import/code",
            "line": line_number,
            "description": "brief description of why this is dead code"
        }}
    ]
}}

If no dead code is found, return: {{"findings": []}}
Only return the JSON, no additional text."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        response_text = response.text.strip()
        if response_text.startswith("`" * 3):
            response_text = response_text.split("\n", 1)[1]
            response_text = response_text.rsplit("`" * 3, 1)[0]
        return json.loads(response_text)
    except Exception as e:
        return {"error": str(e), "findings": []}

def format_findings_markdown(all_findings: list[dict]) -> str:
    """Format all findings as markdown for a GitHub Issue."""
    if not all_findings:
        return "## Stale Code Report\n\nNo dead code detected in this scan."

    markdown = "## Stale Code Report\n\n"
    markdown += f"Found {len(all_findings)} potential issues:\n\n"

    by_type = {}
    for finding in all_findings:
        finding_type = finding.get("type", "unknown")
        if finding_type not in by_type:
            by_type[finding_type] = []
        by_type[finding_type].append(finding)

    type_labels = {
        "unused_function": "Unused Functions",
        "dead_import": "Dead Imports",
        "unreachable_code": "Unreachable Code"
    }

    for finding_type, findings in by_type.items():
        label = type_labels.get(finding_type, finding_type)
        markdown += f"### {label}\n\n"
        for f in findings:
            markdown += f"- **{f.get('name', 'Unknown')}** ({f.get('file', 'unknown')}:{f.get('line', '?')})\n"
            markdown += f"  - {f.get('description', 'No description')}\n\n"

    return markdown

def main():
    """Main function to scan repository and report findings."""
    repo_path = os.environ.get("GITHUB_WORKSPACE", ".")

    print(f"Scanning repository: {repo_path}")

    python_files = get_python_files(repo_path)
    print(f"Found {len(python_files)} Python files")

    all_findings = []
    for i, file_path in enumerate(python_files):
        print(f"Analyzing: {file_path}")
        content = read_file_content(file_path)
        if content.startswith("Error"):
            print(f"  Skipping due to read error")
            continue

        result = analyze_code(content, file_path)

        time.sleep(12)

        if "error" in result:
            print(f"  Analysis error: {result['error']}")
            continue

        for finding in result.get("findings", []):
            finding["file"] = file_path
            all_findings.append(finding)

    markdown_report = format_findings_markdown(all_findings)
    print("\n" + "=" * 50)
    print(markdown_report)

    with open("stale_code_report.md", "w") as f:
        f.write(markdown_report)

    print(f"\nReport saved to stale_code_report.md")
    return all_findings

if __name__ == "__main__":
    findings = main()
    exit(1 if findings else 0)
