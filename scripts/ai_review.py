import sys
import os
from google import genai

# Configure your Gemini API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def review_code(diff_text: str) -> str:
    """Send a code diff to Gemini and return its review."""
    prompt = f"""You are a code reviewer. Review the following code diff and check for:
- Bugs or errors
- Security vulnerabilities (e.g. SQL injection)
- Style and readability issues

If the code looks good, say so.

Code diff to review:

{diff_text}

Provide your review in a clear, structured format."""

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text


if __name__ == "__main__":
    # Check if a filename was passed as a command-line argument
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        with open(diff_file, "r") as f:
            diff_content = f.read()
    else:
        # If no file was provided, read from stdin (e.g. piped input)
        diff_content = sys.stdin.read()

    review = review_code(diff_content)
    print(review)