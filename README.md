# Passiv

> **Automated market pulpit**  
> Passiv ingests live market & crypto data, lets GPT-4 chew on it, then publishes version-tracked posts—no human in the loop. A little affiliate link injection happens as well.

---

## What It Does
1. **Data Ingestion** – Pulls financial data from public APIs (CoinGecko, yFinance, etc.).  
2. **AI Content Generation** – Feeds data into GPT-4 prompts that synthesize a short market recap and informative blog post.  
3. **Versioned Publishing** – Saves each post (and its prompt) in PostgreSQL and exposes it via a lightweight React+Vite front-end.  
4. **Affiliate & Compliance Hooks** – Auto-injects disclaimers and affiliate links.

---

## 🏗️  Tech Stack
| Layer        | Tech                                         | Notes                                     |
|--------------|----------------------------------------------|-------------------------------------------|
| Backend      | **Python 3.11**, Django, Django-REST-Framework | Core APIs & admin                         |
| Workers      | Celery + Redis                               | Scheduled ingestion and GPT tasks         |
| Data Store   | PostgreSQL                                   | Versioned posts & prompt provenance       |
| AI           | OpenAI GPT-4                                 | Prompt templates live in `/prompts`       |
| Front End    | React 18, Vite, Markdown-it                  | Ultra-simple reader UI                    |
| CI/CD        | GitHub Actions                               | Lint → test → build → release             |
| Deploy (dev) | Docker Compose                               | `docker-compose up --build`               |



## License

Licensed under the Business Source License 1.1 — see `LICENSE.md` for full details.
