from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="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")


SYSTEM_PROMPT = """
You are a Fix Suggestion Agent.

Your ONLY job:
1. Suggest how to fix the error
2. Provide corrected code snippet

STRICT RULES:
- Output MUST be valid JSON
- NO markdown
- NO extra explanation
- Keep description SHORT and actionable
- Code must be clean and minimal

Output format:
{
  "description": "Short fix explanation",
  "correctedCode": "Fixed code snippet"
}

Guidelines:
- Prefer minimal fixes (do not rewrite entire code)
- Preserve original logic
- Add checks, corrections, or missing parts
- Make code language-appropriate
"""


def suggest_fix(input_text: str):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            temperature=0.2,  # slight creativity for fixes
            max_tokens=300,
            top_p=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analyze and fix the following code/error:\n\n{input_text}"
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()

        parsed = safe_json_parse(content)

        return normalize_output(parsed)

    except Exception as e:
        return {
            "description": "Agent error occurred",
            "correctedCode": str(e)
        }


# 🛡️ Safe JSON parsing
def safe_json_parse(content: str):
    try:
        return json.loads(content)
    except:
        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            return json.loads(content[start:end])
        except:
            return {
                "description": "Parsing error",
                "correctedCode": content
            }


# 🔒 Normalize output
def normalize_output(result: dict):
    return {
        "description": result.get("description", "No fix suggested"),
        "correctedCode": result.get("correctedCode", "")
    }


# 🔗 Chain-ready wrapper
def run_fix_agent(input_text: str):
    return suggest_fix(input_text)


# 🧪 Test block
if __name__ == "__main__":
    test_inputs = [
        "TypeError: cannot read property 'map' of undefined",
        """
        const user = getUser();
        console.log(user.name);
        const data = user.profile.age;
        """
    ]

    for test in test_inputs:
        print("\nINPUT:", test)
        print("OUTPUT:", run_fix_agent(test))
