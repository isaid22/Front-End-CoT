# Chain-of-Thought (CoT) in Mortgage Affordability

This guide outlines how to present your work on the `check_affordability` endpoint in `main.py` to general audience.

## 1. The High-Level Pitch (The "Why")

Start by establishing the use case. You aren't just using CoT for fun; you are using it for **Financial Explainability**.

*   **The Problem:** Users don't trust a black box that just says "You can't afford this house." They need to know *why* to feel treated fairly.
*   **The Solution:** You used Chain-of-Thought prompting to generate a transparent, step-by-step breakdown of the financial math, acting as a "tutor" rather than just a calculator.

## 2. Walkthrough of Your Implementation (The "How")

When you pull up the code (or describe it), focus on these three specific architectural decisions you made in `check_affordability` (approx. lines 384-424 in `main.py`):

### A. The "Hybrid" Pattern (Crucial Point)
Ref: `main.py` logic where you calculate first, then prompt.

*   **What you did:** You explicitly **pre-calculated** the hard math (`monthly_payment`, `max_monthly_budget`) using Python, *before* calling the LLM.
*   **Why it's smart:** LLMs are bad at pure arithmetic. If you asked the LLM to blindly "calculate if I can afford this," it might hallucinate the numbers.
*   **The CoT angle:** You fed the *correct* answers to the LLM and asked it to **"show its work"** to arrive at those answers. This ensures accuracy while getting the verbal reasoning benefits of the LLM.

### B. The Prompt Engineering
Ref: The `system_prompt` in `check_affordability`.

```python
Instructions:
Walk through the math step-by-step to explain *why* the system determined the affordability status.
...
1. Calculate monthly gross income.
2. Verify the max total debt allowed.
...
```

*   **Talking Point:** You didn't just say "explain this." You gave it a **Structured Reasoning Path**. You forced the model to break the problem down into logical chunks (Income -> Debt -> Budget -> Comparison). This is the definition of standardizing Chain-of-Thought.

### C. The Magic Phrase
Ref: The end of `user_message`.

```python
Answer: Let's think step by step.
```

*   **Talking Point:** You included the classic CoT trigger phrase "Let's think step by step" at the very end of the user message. This primes the model to enter reasoning mode immediately rather than jumping to a conclusion.

## 3. Key Interview Q&A Prep

The manager might ask specific follow-ups. Here is how to answer based on your code:

**Q: Why do you set `temperature=0.1`?**
*   **A:** "For creative writing, I'd use 0.7 or higher. But for financial reasoning where I want the CoT to strictly follow the logic without getting 'creative' with the numbers, I need a deterministic output, so I lowered it to 0.1."

**Q: How do you handle hallucinations in CoT?**
*   **A:** "That's exactly why I implemented the hybrid approach. I don't let the LLM do the math. I pass the `is_affordable` boolean and the calculated `monthly_payment` into the prompt. The LLM's job is purely *narrative generation* based on provided ground truth, which minimizes hallucinations."

**Q: Why is CoT better than a hard-coded string template here?**
*   **A:** "I could have used an f-string, but CoT handles edge cases and tone better. If a user is barely failing affordability, the LLM can explain it with nuance ('You are $50 short...') whereas an f-string template would require writing hundreds of `if/else` logic branches to sound natural."

## 4. Demo Script (If you run the app)

If you demo this:
1.  Enter a home price that is slightly too high for the income.
2.  Show the output.
3.  Say: *"Notice how it doesn't just say 'No'. It says 'First, we take your annual income of $100k... then we deduct debts...' — that narrative structure is the Chain of Thought I engineered into the system prompt."*

## Summary
I implemented a Chain-of-Thought system for mortgage affordability that decouples calculation from reasoning. I used Python for deterministic financial math and engineered a structured LLM prompt to generate step-by-step explanatory narratives, ensuring users understand exactly why a loan was approved or denied.
