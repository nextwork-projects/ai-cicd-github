import os
import sys
from groq import Groq


# Initialize the client with API key from environment variable
client = Groq(api_key=os.environ["GROQ_API_KEY"])


# Define a function that takes a code diff as input
def review_code(diff_text):
    # Multi-line prompt that includes {diff_text}
    # Groq acts as a code reviewer focusing on security, bugs, performance
    prompt = f"""
    You are an experienced code reviewer.
    Please analyze the following code diff for potential security issues,
    bugs, and performance concerns. Provide clear, actionable feedback.


    Code diff:
    {diff_text}
    """

    # Send the prompt to the model and get a response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Return just the text from the response
    return response.choices[0].message.content


# Only run this code when the script is executed directly
if __name__ == "__main__":
    # Check if a filename was passed as a command-line argument
    if len(sys.argv) > 1:
        # Get the filename from sys.argv and read the file
        diff_file = sys.argv[1]
        with open(diff_file, "r") as f:
            diff_content = f.read()
    else:
        # If no filename was passed, read from standard input
        diff_content = sys.stdin.read()

    # Call the review function and print the result
    review = review_code(diff_content)
    print(review)