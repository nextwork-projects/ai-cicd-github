from google import genai
import sys

client = genai.Client()

# Define a function that takes a code diff as input
def gemini_code_review(diff:str):

    # Write a multi-line f-string prompt that includes {diff_text}
    # Tell Gemini to act as a code reviewer and focus on security, bugs, performance
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

    IMPORTANT: At the very end of your review, add a severity summary line in exactly this format:
    SEVERITY_SUMMARY: <level>
    Where <level> is one of: CRITICAL, WARNING, GOOD

    Use CRITICAL if any HIGH severity issues exist.
    Use WARNING if only MEDIUM or LOW severity issues exist.
    Use GOOD if no issues found.

    Code diff to review:

    {diff_text}


    Provide your review in a clear, structured format, ending with the SEVERITY_SUMMARY line."""


    # Send the prompt to the model and get a response
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt
    )

    # Return just the text from the response
    return response.text

def parse_severity(review_text):
    """Extract severity level from the review output."""
    for line in review_text.strip().split("\n"):
        if line.strip().startswith("SEVERITY_SUMMARY:"):
            level = line.split(":", 1)[1].strip().upper()
            if level in ("CRITICAL", "WARNING", "GOOD"):
                return level
    return "WARNING"  # Default to WARNING if parsing fails



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
    review = gemini_code_review(diff_content)
    severity = parse_severity(review)

    print(review)
    # Open severity.txt for writing
    with open("severity.txt", "w") as f:
        # Write the severity string to the file
        f.write(severity)

