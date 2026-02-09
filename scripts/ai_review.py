from google import genai
import sys

client = genai.Client()

# Define a function that takes a code diff as input
def review_code(diff_text):
    prompt = f"""Act as a code reviewer. Here is a code diff:

{diff_text}

Review for:
- Security issues
- Bugs
- Performance issues
- Code style issues
- Code readability issues
- Code maintainability issues
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text

# Only run this code when the script is executed directly
if __name__ == "__main__":
    # Check if a filename was passed as a command-line argument
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        with open(diff_file, "r", encoding="utf-8") as f:
            diff_content = f.read()
    else:
        # If no filename was passed, read from standard input
        diff_content = sys.stdin.read()

    # Call the review function and print the result
    review = review_code(diff_content)  # fixed name
    print(review)
