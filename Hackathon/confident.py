from groq import Groq

# 🔑 Initialize client
client = Groq(api_key="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")


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
            model="openai/gpt-oss-20b",
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

