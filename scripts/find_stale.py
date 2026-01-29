import os
import json
import time
from pathlib import Path
from google import genai

# Create a Gemini client, passing in the API key from environment variables
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def get_python_files(repo_path: str) -> list[str]:
    """Get all Python files in the repository, excluding common ignored directories."""
    python_files = []
    
    # Ignore files in repo like venv, .git, etc
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


def analyze_code_with_gemini(code_content: str, file_path: str) -> dict:
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
        
        # Remove markdown code blocks if Gemini added them
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]      # Remove ```json
            response_text = response_text.rsplit("```", 1)[0]    # Remove closing ```
        
        return json.loads(response_text)
    except Exception as e:
        return {"error": str(e), "findings": []}


def format_findings_as_markdown(all_findings: list[dict]) -> str:
    """Format all findings as markdown for a GitHub Issue."""
    if not all_findings:
        return "## Stale Code Report\n\n✅ No dead code detected in this scan."

    markdown = "## Stale Code Report\n\n"
    markdown += f"Found **{len(all_findings)}** potential issues:\n\n"

    # Group findings by type
    by_type = {}
    for finding in all_findings:
        finding_type = finding.get("type", "unknown")
        if finding_type not in by_type:
            by_type[finding_type] = []
        by_type[finding_type].append(finding)

    type_labels = {
        "unused_function": "🔸 Unused Functions",
        "dead_import": "📦 Dead Imports",
        "unreachable_code": "⚠️ Unreachable Code"
    }

    for finding_type, findings in by_type.items():
        label = type_labels.get(finding_type, finding_type)
        markdown += f"### {label}\n\n"
        for f in findings:
            markdown += f"- **`{f.get('name', 'Unknown')}`** "
            markdown += f"([{f.get('file', 'unknown')}:{f.get('line', '?')}])\n"
            markdown += f"  - {f.get('description', 'No description')}\n\n"

    return markdown


def main():
    """Main function to scan repository and report findings."""
    repo_path = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    print(f"🔍 Scanning repository: {repo_path}")

    python_files = get_python_files(repo_path)
    print(f"📁 Found {len(python_files)} Python files\n")

    all_findings = []
    
    for i, file_path in enumerate(python_files, 1):
        print(f"[{i}/{len(python_files)}] Analyzing: {file_path}")
        content = read_file_content(file_path)
        
        if content.startswith("Error"):
            print(f"  ⚠️  Skipped (read error)")
            continue

        result = analyze_code_with_gemini(content, file_path)

        if "error" in result:
            print(f"  ❌ Analysis error: {result['error']}")
            continue

        findings_count = len(result.get("findings", []))
        if findings_count > 0:
            print(f"  🔴 Found {findings_count} issue(s)")
            for finding in result.get("findings", []):
                finding["file"] = file_path
                all_findings.append(finding)
        else:
            print(f"  ✅ No issues found")
        
        # Rate limiting - be nice to the API
        time.sleep(1)

    # Generate markdown report
    markdown_report = format_findings_as_markdown(all_findings)
    
    print("\n" + "=" * 60)
    print(markdown_report)
    print("=" * 60)

    # Save report to file
    report_filename = "stale_code_report.md"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(markdown_report)

    print(f"\n💾 Report saved to {report_filename}")
    
    return all_findings


if __name__ == "__main__":
    findings = main()
    # Exit with error code if dead code was found
    exit(1 if findings else 0)
