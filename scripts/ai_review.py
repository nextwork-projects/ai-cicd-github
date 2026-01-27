from google import genai
import os
import sys

# Gemini SDK looks for GOOGLE_API_KEY by default, but we support both.
api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def review_code(diff_text: str) -> str:
    """Send a code diff to Gemini for review."""
    prompt = f"""You are an expert code reviewer. Review the following code diff and provide feedback.

Focus on:
1. Security vulnerabilities
2. Bug risks
3. Performance issues
4. Best practice violations

For each issue found, provide:
- Severity: HIGH / MEDIUM / LOW
- Description of the issue
- Suggested fix

If the code looks good, say so.

Code diff to review:

{diff_text}

Provide your review in a clear, structured format."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        with open(diff_file, "r", encoding="utf-8") as f:
            diff_content = f.read()
    else:
        diff_content = sys.stdin.read()

    print(review_code(diff_content))
