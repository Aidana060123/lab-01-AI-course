import os

import json
import time
from google import genai
from texts import CORPUS

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-3.6-flash"


def count_tokens(text):
    result = client.models.count_tokens(
        model=MODEL,
        contents=text
    )
    return result.total_tokens


def generate_answer(text):
    for attempt in range(5):
        try:
            return client.models.generate_content(
                model=MODEL,
                contents=text
            )
        except Exception as e:
            print(f"Attempt {attempt + 1}/5 failed: {e}")
            if attempt < 4:
                print("Waiting 5 seconds and trying again...")
                time.sleep(5)
            else:
                raise


results = {}

for lang in ["en", "ru", "kk"]:
    print("\n" + "=" * 60)
    print(lang.upper())

    complaint = CORPUS["complaint"][lang]

    input_tokens = count_tokens(complaint)
    print("Input tokens:", input_tokens)

    response = generate_answer(complaint)

    output_text = response.text or ""
    output_tokens = count_tokens(output_text)

    print("Output tokens:", output_tokens)
    print("Answer:")
    print(output_text)

    results[lang] = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "answer": output_text
    }

with open("measurements.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("DONE — measurements.json saved")