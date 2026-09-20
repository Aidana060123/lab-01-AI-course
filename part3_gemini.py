
# PART 3 -- Gemini cost calculation
# Gemini 3.6 Flash
# Prices valid through Dec 31, 2026:
# Input  = $0.75 per 1M tokens
# Output = $3.75 per 1M tokens

import json

INPUT_PRICE = 0.75
OUTPUT_PRICE = 3.75

REQUESTS_PER_DAY = 5000
DAYS_PER_YEAR = 365

with open("measurements.json", "r", encoding="utf-8") as f:
    measurements = json.load(f)

print("=" * 70)
print("PART 3 -- GEMINI 3.6 FLASH COST")
print("=" * 70)

total_annual = 0

for lang in ["en", "ru", "kk"]:
    input_tokens = measurements[lang]["input_tokens"]
    output_tokens = measurements[lang]["output_tokens"]

    cost_per_request = (
        input_tokens / 1_000_000 * INPUT_PRICE
        + output_tokens / 1_000_000 * OUTPUT_PRICE
    )

    annual_cost = (
        cost_per_request
        * REQUESTS_PER_DAY
        * DAYS_PER_YEAR
    )

    total_annual += annual_cost

    print(f"\n{lang.upper()}")
    print("-" * 40)
    print("Input tokens per request :", input_tokens)
    print("Output tokens per request:", output_tokens)
    print(f"Cost per request         : ${cost_per_request:.6f}")
    print(f"Annual cost at {REQUESTS_PER_DAY:,} requests/day: ${annual_cost:,.2f}")

print("\n" + "=" * 70)
print("TOTAL if 5,000 EN + 5,000 RU + 5,000 KK requests are made every day")
print(f"Annual cost: ${total_annual:,.2f}")
print("=" * 70)
