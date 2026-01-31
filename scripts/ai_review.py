from google import genai
import sys

client = genai.Client()

def ai_review(code: str) -> str:
    """Review the code using AI."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=code,
    )
    return response.text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        with open(diff_file, "r") as f:
            diff_content = f.read()
    else:
        diff_content = sys.stdin.read()

    review = ai_review(diff_content)
    print(review)
