from google import genai
# from dotenv import load_dotenv
import sys

# load_dotenv()  # Loads variables from .env into the environment

client = genai.Client()  # Now it can find GEMINI_API_KEY


# Define a function that takes a code diff as input
def review_code(diff_text: str):

    # Write a multi-line f-string prompt that includes {diff_text}
    # Tell Gemini to act as a code reviewer and focus on security, bugs, performance
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

# Only run this code when the script is executed directly
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
