import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def build_prompt(user_input: str) -> str:
    return f"""
You are an intelligent billing assistant AI.

Your job is to extract one or more actions from the user's message.

Each action must include:
- intent: one of ["query_bill", "query_detailed_bill", "make_payment", "add_usage"]
- parameters:
    - subscriberNo (int)
    - month (1–12)
    - year (e.g., 2024)
    - if intent is "add_usage", include:
        - usageType: "internet" or "phone"
        - amount: an integer only. Do NOT do any unit conversion. 
          For example, if the user says "15 GB", just return 15.
          DO NOT return 15 * 1024 or similar expressions.

If any parameter is missing, respond like this:
{{ "intent": "missing_info", "missing": ["subscriberNo", "month"] }}

Only include make_payment if the user clearly says "pay" or "make a payment".

Respond ONLY with raw, valid JSON. DO NOT include any explanation, markdown, or natural language.

User message:
\"{user_input}\"
"""

def ask_openai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = response.choices[0].message.content.strip()

        # Ekrana yaz
        print("DEBUG > LLM response:", content)

        # Dosyaya yaz
        with open("llm_debug.json", "w", encoding="utf-8") as f:
            f.write(content)

        return content

    except Exception as e:
        print("❌ OpenAI API Error:", e)
        return ""
