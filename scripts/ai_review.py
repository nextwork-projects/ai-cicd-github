from google import genai
import sys

client = genai.Client()


def review_code(diff_text):

    # 1. Define the persona and the task
    prompt = f"""
    Act as an expert Senior Code Reviewer. 
    Review the following code diff for:
    - Security vulnerabilities (e.g., hardcoded secrets)
    - Logic bugs or edge cases
    - Performance bottlenecks
    
    Code Diff:
    {diff_text}
    """

    # 2. Call the model (Gemini 2.0 Flash is great for speed/coding)
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=prompt
    )

    # 3. Return the text content specifically
    return response.text


if __name__ == "__main__":
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        with open(diff_file, "r") as f:
            diff_content = f.read()
    else:
        diff_content = sys.stdin.read()

    review = review_code(diff_content)
    print(review)
