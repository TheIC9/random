
from groq import Groq

# 🔑 Initialize client
client = Groq(api_key="YOUR_GROQ_API_KEY")


SYSTEM_PROMPT = """
You are a Confidence Scoring Agent.

Your ONLY job:
- Analyze the given debugging result
- Output a confidence score between 0 and 1

STRICT RULES:
- Output MUST be ONLY a number
- NO JSON
- NO explanation
- NO text
- Example: 0.87

Scoring Guidelines:
- 0.9 - 1.0 → Very clear error, precise fix
- 0.7 - 0.89 → Good confidence, minor ambiguity
- 0.5 - 0.69 → Moderate confidence
- 0.3 - 0.49 → Low confidence
- 0.0 - 0.29 → Very uncertain
"""


def get_confidence(input_text: str):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0,  # deterministic
            max_tokens=10,
            top_p=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Evaluate confidence for this debugging result:\n\n{input_text}"
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        return normalize_score(content)

    except Exception:
        return 0.5  # fallback neutral


# 🔒 Normalize score safely
def normalize_score(content: str):
    try:
        score = float(content)

        # Clamp between 0 and 1
        if score < 0:
            return 0.0
        elif score > 1:
            return 1.0
        else:
            return round(score, 2)

    except:
        return 0.5  # fallback


# 🔗 Chain-ready wrapper
def run_confidence_agent(full_result: dict):
    # Convert full pipeline result into text
    input_text = str(full_result)
    return get_confidence(input_text)


# 🧪 Test block
if __name__ == "__main__":
    sample_result = {
        "type": "Runtime Error",
        "message": "cannot read property 'map' of undefined",
        "line": 22,
        "snippet": "user.profile.age",
        "severity": "High",
        "language": "JavaScript",
        "root_cause": "Object is null before method call",
        "description": "Add null check before accessing property",
        "correctedCode": "if (user && user.profile) { const data = user.profile.age; }"
    }

    score = run_confidence_agent(sample_result)
    print("Confidence Score:", score)




from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="YOUR_GROQ_API_KEY")


SYSTEM_PROMPT = """
You are an Error Classification Agent.

Your ONLY job:
1. Classify the error into a category
2. Assign severity level
3. Detect programming language

STRICT RULES:
- Output MUST be valid JSON
- NO explanations
- NO markdown
- ONLY one JSON object

Categories:
- Syntax Error
- Runtime Error
- Logical Error
- Dependency Error
- Configuration Error
- Unknown Error

Severity Levels:
- Low
- Medium
- High
- Critical

Output format:
{
  "type": "Error Category",
  "severity": "Severity Level",
  "language": "Programming Language"
}

If unknown:
{
  "type": "Unknown Error",
  "severity": "Medium",
  "language": "Unknown"
}
"""


def classify_error(input_text: str):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0,
            max_tokens=200,
            top_p=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analyze and classify the following error/code:\n\n{input_text}"
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()

        parsed = safe_json_parse(content)

        return normalize_output(parsed)

    except Exception as e:
        return {
            "type": "Unknown Error",
            "severity": "Medium",
            "language": f"AgentError: {str(e)}"
        }


# 🛡️ Robust JSON parsing
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
                "type": "Unknown Error",
                "severity": "Medium",
                "language": "ParsingError"
            }


# 🔒 Normalize output
def normalize_output(result: dict):
    return {
        "type": result.get("type", "Unknown Error"),
        "severity": result.get("severity", "Medium"),
        "language": result.get("language", "Unknown")
    }


# 🔗 Chain-ready wrapper
def run_classification_agent(input_text: str):
    return classify_error(input_text)


# 🧪 Test block
if __name__ == "__main__":
    test_inputs = [
        "TypeError: cannot read property 'map' of undefined",
        "SyntaxError: invalid syntax in Python file",
        "NullPointerException at line 42 in Java",
        "ModuleNotFoundError: No module named 'numpy'"
    ]

    for test in test_inputs:
        print("\nINPUT:", test)
        print("OUTPUT:", run_classification_agent(test))





from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="YOUR_GROQ_API_KEY")


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
            model="llama3-70b-8192",
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




from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="YOUR_GROQ_API_KEY")


SYSTEM_PROMPT = """
You are an Error Line Identification Agent.

Your ONLY job:
1. Identify the exact line number where the error occurs
2. Extract the failing code snippet from that line

STRICT RULES:
- Output MUST be valid JSON
- NO explanations
- NO markdown
- ONLY one JSON object

Output format:
{
  "line": <line_number>,
  "snippet": "exact code causing error"
}

If line cannot be determined:
{
  "line": -1,
  "snippet": "Not found"
}
"""


def identify_error_line(input_text: str):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0,
            max_tokens=200,
            top_p=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analyze the following code/logs and find the exact failing line:\n\n{input_text}"
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()

        parsed = safe_json_parse(content)

        return normalize_output(parsed)

    except Exception as e:
        return {
            "line": -1,
            "snippet": f"AgentError: {str(e)}"
        }


# 🛡️ Robust JSON parsing
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
                "line": -1,
                "snippet": content
            }


# 🔒 Normalize output (guarantee structure)
def normalize_output(result: dict):
    return {
        "line": result.get("line", -1),
        "snippet": result.get("snippet", "Not found")
    }


# 🔗 Chain-ready wrapper
def run_line_agent(input_text: str):
    return identify_error_line(input_text)


# 🧪 Test block
if __name__ == "__main__":
    test_input = """
    20 | const user = getUser();
    21 | console.log(user.name);
    22 | const data = user.profile.age;
    TypeError: Cannot read property 'profile' of undefined at line 22
    """

    result = run_line_agent(test_input)
    print(result)



from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="YOUR_GROQ_API_KEY")


SYSTEM_PROMPT = """
You are an Explanation Agent.

Your ONLY job:
- Convert technical errors into human-friendly explanations

You must return TWO formats:
1. Simple (for beginners)
2. Detailed (for developers)

STRICT RULES:
- Output MUST be valid JSON
- NO markdown
- NO extra text
- Simple = very short, easy to understand (1 line)
- Detailed = clear technical explanation (2-3 lines max)

Output format:
{
  "simple": "Beginner-friendly explanation",
  "detailed": "Technical explanation"
}
"""


def generate_explanation(input_text: str):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0.3,  # slight creativity for clarity
            max_tokens=250,
            top_p=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Explain the following error/code:\n\n{input_text}"
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()

        parsed = safe_json_parse(content)

        return normalize_output(parsed)

    except Exception as e:
        return {
            "simple": "Unable to explain error",
            "detailed": f"AgentError: {str(e)}"
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
                "simple": content,
                "detailed": content
            }


# 🔒 Normalize output
def normalize_output(result: dict):
    return {
        "simple": result.get("simple", "No simple explanation available"),
        "detailed": result.get("detailed", "No detailed explanation available")
    }


# 🔗 Chain-ready wrapper
def run_explanation_agent(input_text: str):
    return generate_explanation(input_text)


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
        print("OUTPUT:", run_explanation_agent(test))






from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="YOUR_GROQ_API_KEY")


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
            model="llama3-70b-8192",
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







from groq import Groq
import json

# 🔑 Initialize client
client = Groq(api_key="YOUR_GROQ_API_KEY")


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
            model="llama3-70b-8192",
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





def run_stackheal_pipeline(input_text: str):
    """
    Orchestrator for StackHeal AI pipeline.
    Runs all 7 agents in order and returns combined structured output.
    """
    final_result = {}

    # 1️⃣ Detect error
    error_result = run_error_agent(input_text)
    final_result.update(error_result)

    # 2️⃣ Identify error line
    line_result = run_line_agent(input_text)
    final_result.update(line_result)

    # 3️⃣ Classify error
    classification_result = run_classification_agent(input_text)
    final_result.update(classification_result)

    # 4️⃣ Root cause analysis
    root_cause_result = run_root_cause_agent(input_text)
    final_result.update(root_cause_result)

    # 5️⃣ Suggest fix
    fix_result = run_fix_agent(input_text)
    final_result.update(fix_result)

    # 6️⃣ Explanation (simple + detailed)
    explanation_result = run_explanation_agent(input_text)
    final_result.update(explanation_result)

    # 7️⃣ Confidence score
    confidence_score = run_confidence_agent(final_result)
    final_result["confidence"] = confidence_score

    return final_result


# 🧪 Test block
if __name__ == "__main__":
    test_input = """
    const user = getUser();
    console.log(user.name);
    const data = user.profile.age;
    TypeError: Cannot read property 'profile' of undefined at line 22
    """

    result = run_stackheal_pipeline(test_input)
    print("\nFINAL STACKHEAL AI OUTPUT:\n")
    import json
    print(json.dumps(result, indent=2))