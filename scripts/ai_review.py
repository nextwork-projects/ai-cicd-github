from google import genai
import sys
import os

# Get API key from environment variable
api_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "Missing API key! Please set GOOGLE_AI_API_KEY or GEMINI_API_KEY environment variable.\n"
        "You can get an API key from: https://aistudio.google.com/apikey"
    )

client = genai.Client(api_key=api_key)

def review_code(diff_text):
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
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text

if __name__ == "__main__":
    # Check if a filename was passed as a command-line argument
    if len(sys.argv) > 1:
        # Get the filename from sys.argv and read the file
        diff_file = sys.argv[1]
        with open(diff_file, "r") as f:
            diff_content = f.read()
    # If no filename was passed, read from standard input
    else:
        diff_content = sys.stdin.read()

    # Call the review function and print the result
    review = review_code(diff_content)
    print(review)
