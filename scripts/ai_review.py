from google import genai
import sys

client = genai.Client()

    
def ReviewCode(diff_code):

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

Keep The reveiew Concise and to the point. Do not provide feedback on code that has been deleted, only on new or modified code.

Code diff to review:

{diff_code}


Provide your review in a clear, structured format."""

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        with open(diff_file, 'r') as f:
            diff_code = f.read()
    else:
        diff_code = sys.stdin.read()

    review = ReviewCode(diff_code)
    print(review)