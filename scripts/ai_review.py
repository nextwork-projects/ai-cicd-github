import requests
import sys
import os
import json
from dotenv import load_dotenv

# Load environment
load_dotenv(override=True)
api_key = os.environ.get('GEMINI_API_KEY')

if not api_key:
    print("ERROR: GEMINI_API_KEY not found!")
    sys.exit(1)

api_key = api_key.strip()
print(f"API Key loaded: {api_key[:10]}...{api_key[-4:]}")

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

    # Use the correct model name from the list
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    print("Sending request to Gemini API...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']

if __name__ == "__main__":
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        with open(diff_file, "r") as f:
            diff_content = f.read()
    else:
        diff_content = sys.stdin.read()

    print("\nGenerating review...\n")
    review = review_code(diff_content)
    print("\n=== CODE REVIEW ===\n")
    print(review)