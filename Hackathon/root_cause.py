from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="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")


SYSTEM_PROMPT = """
You are a Root Cause Analysis Agent.

Your ONLY job:
- Explain WHY the error occurs

STRICT RULES:
- Output MUST be valid JSON
- NO markdown
- NO extra explanation
- Keep response SHORT and precise (1 line preferred)

Output format:
{
  "root_cause": "Concise reason why error happens"
}

Examples:
- "Object is null before method call"
- "Variable used before initialization"
- "Incorrect data type passed to function"
- "Missing dependency causes module load failure"
"""


def analyze_root_cause(input_text: str):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            temperature=0,
            max_tokens=100,
            top_p=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analyze the following error/code and find root cause:\n\n{input_text}"
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()

        parsed = safe_json_parse(content)

        return normalize_output(parsed)

    except Exception as e:
        return {
            "root_cause": f"AgentError: {str(e)}"
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
                "root_cause": content
            }


# 🔒 Normalize output
def normalize_output(result: dict):
    return {
        "root_cause": result.get(
            "root_cause",
            "Unable to determine root cause"
        )
    }


# 🔗 Chain-ready wrapper
def run_root_cause_agent(input_text: str):
    return analyze_root_cause(input_text)


# 🧪 Test block
if __name__ == "__main__":
    test_inputs = [
        "TypeError: cannot read property 'map' of undefined",
        "NullPointerException at line 42",
        "SyntaxError: invalid syntax",
        "ModuleNotFoundError: No module named 'pandas'"
    ]

    for test in test_inputs:
        print("\nINPUT:", test)
        print("OUTPUT:", run_root_cause_agent(test))