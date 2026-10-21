# AI features in the product

Read this when the product itself uses AI: language models, image or speech models, recommendation or prediction. Record the outcome in an ADR titled "AI architecture" and the risks in risks.md.

## 1. Is AI needed here?
Use plain code when the rules are known and stable (calculations, routing, validation, scheduling). Use AI for language, ambiguity, messy inputs, summarizing and generation. Ask the owner what happens when the AI is wrong; that answer sets how much checking, review and human approval the design needs.

## 2. Use the lowest rung that works
1. A single model call with structured output (a JSON schema; the major providers support this natively), validated by your code.
2. Retrieval over your own data (search, then answer with citations) when answers depend on private or changing information. Start with PostgreSQL full-text search plus pgvector before adding a separate vector database.
3. Tool use in a single agent loop, with tools that are narrow and permissioned.
4. Multiple cooperating agents, only when evaluations show simpler designs fall short.
Fine-tune only after evaluations show prompting and retrieval cannot reach the target and you have good training data.

## 3. Model and provider
- Compare capability, cost per task, latency, context size, data policy (retention, use for training, regions) and reliability. Verify the current model lineup and prices at decision time; they change every few months.
- Put the provider behind a thin interface in your code so you can switch or add a fallback.
- Prefer providers and settings that do not retain or train on customer data when data is personal or confidential.

## 4. Untrusted input and permissions
- Treat user text, uploaded files, retrieved documents, web pages and tool results as data, never as instructions. Prompt injection hides commands in exactly these places.
- Give the model the narrowest tools and data access the task needs. Scope every tool call to the current user and tenant.
- Require human approval for consequential or irreversible actions: sending messages, spending money, deleting or changing records, anything legal, medical or financial.
- Use the OWASP Top 10 for LLM Applications and for Agentic Applications as review checklists.

## 5. Output handling
- Ask for structured output and validate it in code; reject or retry on invalid output.
- Never execute model output directly (code, SQL, shell, HTML) without validation and sandboxing.
- Show uncertainty and sources to users where wrong answers matter.

## 6. Evaluations before launch
- Build a set of 20–100 realistic cases with expected results, including tricky and adversarial ones.
- Run it on every prompt, model or retrieval change, like a test suite.
- After launch, sample real outputs, collect user feedback, and add failures to the set.

## 7. Cost, latency and abuse
- Estimate tokens per action × actions per user per month × users. Add it to the cost sketch.
- Set per-user and per-tenant rate limits and monthly spend caps, with alerts.
- Use caching, smaller models for simple steps, and streaming for perceived speed.
- Moderate user-facing generation where misuse is plausible.

## 8. Privacy
- Know exactly which data is sent to the provider. Minimize it; redact personal data where possible.
- Check the provider's data processing terms and retention options against the project's obligations.

## 9. Failure and fallback
- Timeouts, retries with backoff, and a degraded mode (for example, the feature hides or falls back to manual).
- A second provider only when the feature is critical enough to justify the extra testing.

## 10. Observability
- Log inputs and outputs (with personal data redacted), latency, token usage, cost, errors and user feedback per feature.
- Track quality over time with the evaluation set, so model or prompt drift is caught.
