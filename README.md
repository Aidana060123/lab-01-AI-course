# Lab 01 — The price of one request

Week 1 · LLMs, Agentic AI and Reinforcement Learning · Narxoz University

You will measure what the same piece of work costs in English, Russian and
Kazakh, and you will get the number by measuring it rather than by looking it
up. The tokenizer is the reason the three numbers differ, and it is the first
engineering constraint in this course that has a currency attached.

## Setup

Requires **Python 3.10+** — the `anthropic` SDK's 1.x line dropped 3.9.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then paste in a real ANTHROPIC_API_KEY
```

`.env` is gitignored; `.env.example` is the template that ships in the repo.
`part2_measure.py` loads `.env` automatically — no need to `export` anything.
The key must be scoped to a **workspace** in the Console, not the
organization level, or the API rejects every request with a 400 asking for
an `anthropic-workspace-id` header.

No API key is needed for Part 0, Part 1 or Part 3.

## Part 0 — the OpenAI pair (no key, no network, no cost)

```bash
python3 part0_tokenizers.py
```

Anthropic publishes no offline tokenizer, so Part 2 can only show Claude's
own counts. This script fills that gap with `tiktoken`'s `o200k_base` and
`cl100k_base` — the two public tokenizers that bracket the six-tokenizer
spread shown in lecture 2 (`o200k_base` kindest to Kazakh, `cl100k_base`
harshest). It reproduces that lecture's numbers exactly, corpus item by
corpus item — a good sanity check that nothing has drifted.

## Part 1 — predict (no key, no network, no cost)

```bash
python3 part1_offline.py
```

Characters, UTF-8 bytes and words for the three texts, in three languages.
Write down your prediction for the token ratio **before** Part 2 runs. A
prediction you did not write down is a prediction you will not remember
getting wrong.

## Part 2 — measure (instructor's key, on the projector)

```bash
python3 part2_measure.py --call
```

Two things happen. `count_tokens` asks the tokenizer how many tokens each text
costs — free, and the model never runs, including a combined count for the
actual request shape (system prompt + complaint, one call) that Part 3 prices.
Then the same complaint is actually answered in each of the three languages,
so the *answer* length is measured too rather than assumed. Results land in
`measurements.json`.

`claude-opus-5` runs adaptive thinking by default, and thinking tokens are
billed at the output rate but never shown in the reply — on this corpus they
ran 175–345 tokens per answer before a single visible word. That is exactly
the invisible-cost trap lecture 2 warns about; it is not a bug to fix by
turning thinking off. `MAX_TOKENS` (2048) is sized to clear it with margin —
watch for `stop_reason: max_tokens` in the output, which means an answer got
cut off and the measurement for that language is unusable.

Without `--call` the script only counts tokens and spends nothing; Part 3 then
has to assume an answer length and will say so loudly.

## Part 3 — cost it out (no key)

```bash
python3 part3_cost.py
python3 part3_cost.py --requests-per-day 5000
```

Per-request cost across four models, the annual bill at a volume you choose,
and the two ratios that get confused in public: the input-token ratio (a
property of the tokenizer) and the total-bill ratio (what you actually pay,
which moves with answer length).

## What you hand in

One page.

1. Your Part 1 prediction, and the measured value next to it.
2. The annual cost table for a volume you justify in one sentence.
3. Which model you would put in production for a Kazakh-language support
   queue, and the cost and quality argument for it.
4. One sentence naming a cost lever this lab did **not** use.

## Extend it — task ideas

For a follow-up assignment, roughly cheapest first.

**No key, no network — edit `texts.py`:**
- Add your own EN/RU/KK item (a contract clause, an NBK notice, a real
  complaint) and predict its ratio before running Part 1.
- Code-switched KK/RU in one sentence vs. the pure-language version.
- Numbers and currency (₸, %, IBAN, dates) instead of prose.
- Latin-script Kazakh vs. the same sentence in Cyrillic.

**`count_tokens` only, effectively free — Part 2 without `--call`:**
- The same content as JSON/a table instead of prose — measure the
  structuring overhead.
- Shorten or lengthen `system_prompt` and watch `request_tokens` move.

**One real call, a few cents — Part 2/3:**
- Implement the cost lever you named in your write-up (prompt caching on
  `system_prompt` is the obvious one) and re-measure.
- Cap the answer with "reply in one sentence" and compare output tokens
  across languages.
- The same complaint on Haiku vs. Opus — price and answer quality side by
  side.

Keep any new corpus item semantically parallel across the three languages,
or the comparison measures translation length, not tokenization.

## Files

| File | Needs a key | What it does |
|---|---|---|
| `texts.py` | no | The parallel corpus: three texts × three languages |
| `prices.py` | no | List prices, with source URL and the date they were checked |
| `part0_tokenizers.py` | no | `tiktoken` counts on `o200k_base` and `cl100k_base` |
| `part1_offline.py` | no | Characters, bytes, words, and the prediction prompt |
| `part2_measure.py` | **yes** | `count_tokens` for everything; one real answer per language |
| `part3_cost.py` | no | Reads `measurements.json`, prints the cost tables |

`measurements.json` is produced by Part 2. It is not in the repository, on
purpose: token counts are model-specific and dated, and a stale file is worse
than no file. `measurements.example.json` **is** in the repository — a
reference run from 2026-09-12, so Part 3 has something to work against
before your own Part 2 run, or if the projector key is unavailable. Copy it
to `measurements.json` to use it: `cp measurements.example.json measurements.json`.

## Notes for the instructor

- Part 2 runs once, on the projector. Hand `measurements.json` to the students
  afterwards — without it Part 3 refuses to run, on purpose, rather than
  inventing token counts.
- `MAX_TOKENS` in `part2_measure.py` is 2048. It used to be 512, which was not
  enough headroom once adaptive thinking is accounted for — thinking tokens
  ran 175–345 per answer on this corpus, and 512 cut answers off mid-sentence
  (`stop_reason: max_tokens`). Do not lower it back down without checking
  `stop_reason` on every language first.
- The API key must be **workspace-scoped** in the Console. An
  organization-level key is rejected outright (400, missing
  `anthropic-workspace-id`) before it spends anything.
- `--call` makes three requests. At list price on `claude-opus-5` that is a
  few US cents in total — in the reference run, 145–317 input tokens and
  955–1,337 output tokens per language, so under $0.10 total even before any
  volume discount.
- Prices in `prices.py` were checked on 2026-09-12 against the source named in
  the module docstring. Re-check before teaching; if they moved, the lab still
  works, but the slide numbers will not match.
- The Russian and Kazakh wordings in `texts.py` are a starting point. Replace
  them with your own if you prefer — but keep the three versions semantically
  parallel, or the comparison measures translation length instead of
  tokenization.
- `request_tokens` in `measurements.json` is a **combined** count (system
  prompt + complaint, one `count_tokens` call) — not the sum of the two
  items' standalone counts. Summing standalone counts double-counts each
  message's per-call framing overhead (about 5 tokens out of 145 on the
  English request, roughly 3%, proportionally larger on short texts). Part 3
  reads `request_tokens` directly; it will refuse to run on an older
  `measurements.json` that predates this field.
