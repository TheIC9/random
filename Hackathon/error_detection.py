from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="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")


SYSTEM_PROMPT = """
You are a strict Error Detection Agent.

Your ONLY job:
1. Detect if an error exists in the input
2. Identify the error type (e.g., TypeError, SyntaxError, NullPointerException, etc.)
3. Extract the exact error message

STRICT RULES:
- Output MUST be valid JSON
- NO markdown
- NO explanation
- NO extra text
- ONLY one JSON object

Output format:
{
  "type": "ErrorType",
  "message": "Exact error message"
}

If no error is found:
{
  "type": "NoError",
  "message": "No error detected"
}
"""


def detect_error(input_text: str):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            temperature=0,
            max_tokens=200,
            top_p=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analyze the following input and detect error:\n\n{input_text}"
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()

        # 🔒 Safe JSON parsing
        parsed = safe_json_parse(content)

        return parsed

    except Exception as e:
        return {
            "type": "AgentError",
            "message": str(e)
        }


# 🛡️ Robust JSON parser (handles edge cases)
def safe_json_parse(content: str):
    try:
        return json.loads(content)
    except:
        # Attempt recovery if model slightly breaks format
        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            return json.loads(content[start:end])
        except:
            return {
                "type": "ParsingError",
                "message": content
            }


# 🔗 Chain-ready wrapper
def run_error_agent(input_text: str):
    result = detect_error(input_text)

    # Normalize output (guarantee keys exist)
    return {
        "type": result.get("type", "UnknownError"),
        "message": result.get("message", "")
    }


# 🧪 Test block
if __name__ == "__main__":
    test_cases = [
        "TypeError: cannot read property 'map' of undefined",
        "NullPointerException at line 42",
        "SyntaxError: invalid syntax",
        "Everything executed successfully"
    ]

    for test in test_cases:
        print("\nINPUT:", test)
        print("OUTPUT:", run_error_agent(test))

