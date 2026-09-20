# Lab 01 – The Price of One Request

## 1. Prediction and Results

In this lab, I compared English, Russian and Kazakh.

In Part 1, I used the text size in bytes to make my prediction.

For the complaint:
- English: 300 bytes
- Russian: 576 bytes
- Kazakh: 640 bytes

My prediction was:
- Russian / English = 1.92x
- Kazakh / English = 2.13x

Then I tested the same task with Gemini 3.6 Flash.

The measured input tokens were:
- English: 60 tokens
- Russian: 79 tokens
- Kazakh: 149 tokens

The measured input-token ratios were:
- Russian / English = 1.32x
- Kazakh / English = 2.48x

The prediction and the real result were different. This shows that bytes and tokens are related, but they are not the same.

## 2. Annual Cost

I used 5,000 requests per day because this can represent a support service with many daily requests.

| Language | Input tokens | Output tokens | Annual cost |
|---|---:|---:|---:|
| English | 60 | 576 | $4,024.12 |
| Russian | 79 | 781 | $5,453.10 |
| Kazakh | 149 | 1,121 | $7,875.79 |

The total annual cost for all three languages is $17,353.01.

In this experiment, Kazakh had the highest cost because it used more tokens.

## 3. Model for Kazakh Support

For this lab, I used Gemini 3.6 Flash.

I would consider Gemini 3.6 Flash for a Kazakh-language support queue because cost is important when there are many requests.

However, quality is also important. The model sometimes added information that was not provided in the original task. Before real production use, I would test more Kazakh examples and check the quality of the answers.

## 4. Cost Reduction

One way to reduce the cost is to limit the answer length. Shorter answers use fewer output tokens, so the cost can be lower.
