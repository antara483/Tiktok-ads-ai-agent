
# TikTok Ads AI Agent (CLI)

## Overview

This project is a **CLI-based AI Agent** that helps a user **create and submit a TikTok Ad configuration through a conversation**.

The focus of this project is **not UI or model training**, but:

* Prompt design for structured output
* Reasoning about external APIs
* Enforcing business rules (guardrails)
* Handling unreliable or failing APIs gracefully

The agent guides the user step-by-step, validates inputs, generates a structured ad payload using **Gemini**, and simulates submission to the TikTok Ads API.

---

## High-Level Architecture

```
User (CLI)
   ↓
AI Agent (Python)
   ├── OAuth (mocked Authorization Code flow)
   ├── Conversation & rule enforcement
   ├── Gemini (structured JSON generation)
   └── Mock TikTok Ads API (submission + error handling)
```

---

## How OAuth Is Handled

### OAuth Model Used

This project implements a **mocked OAuth Authorization Code flow** that mirrors TikTok Ads OAuth behavior.

### Flow

1. User initiates connection
2. Agent simulates redirect to TikTok OAuth
3. An **authorization code** is generated
4. The code is exchanged for an **access token**
5. The token is stored with:

   * Expiry time
   * Permission scope (`ads`)

### Why OAuth Is Mocked

* TikTok Ads is not available in all regions (e.g., India)
* Business verification is required for real access
* The assignment focuses on **reasoning**, not live ad creation

### OAuth Error Handling

The agent detects and explains:

* Invalid client credentials
* Expired or revoked token
* Missing Ads permission scope
* Geo-restriction (403)

Instead of raw errors, the agent provides:

* Clear explanation
* Suggested corrective action

---

## Conversational Ad Creation Flow

The agent collects ad inputs step-by-step via CLI:

1. Campaign Name (required, min 3 chars)
2. Objective (`Traffic` or `Conversions`)
3. Ad Text (required, max 100 chars)
4. CTA (required)
5. Music option (conditional logic enforced)

Each step is validated before moving forward.

---

## Music Logic (Primary Evaluation Area)

The agent supports **all three required music cases**:

### Case A: Existing Music ID

* User enters a Music ID
* Agent validates it via a mocked API
* If invalid:

  * Explains the failure
  * Prompts the user to choose again

### Case B: Uploaded / Custom Music

* Agent asks if the user wants to upload custom music
* Upload is simulated
* A mock `music_id` is generated
* Validation happens before submission

### Case C: No Music

* Allowed **only if Objective = Traffic**
* Explicitly blocked if Objective = Conversions
* Rule enforced **before submission**

This logic is handled deterministically in Python, not by the LLM.

---

## Prompt Design & Structured Output

### Prompt Design

Gemini is used **only where it adds value**:

* Converting collected inputs into a structured JSON payload

The system prompt enforces:

* JSON-only output
* No invented values
* Strict schema compliance

### Structured Output Format

```json
{
  "campaign_name": "...",
  "objective": "...",
  "creative": {
    "text": "...",
    "cta": "...",
    "music_id": "..."
  }
}
```

### Safety Measures

* Markdown fences (```json) are stripped
* Output is parsed using `json.loads`
* If Gemini fails, a deterministic fallback payload is used

---

## Internal Reasoning (Explicit & Lightweight)

The agent maintains a **lightweight internal reasoning log** that records:

* Objective selection
* Music rule enforcement
* Validation decisions
* Fallback usage

This reasoning is:

* Explicitly printed
* Deterministic
* Not chain-of-thought

This satisfies the requirement to separate:

* User conversation
* Internal reasoning
* Final ad payload

---

## API Assumptions & Mocks

Because live TikTok Ads access is not required, the following APIs are mocked:

### Mocked APIs

* TikTok OAuth (Authorization Code flow)
* TikTok Ads submission API
* Music validation API

### Simulated Failures

* Invalid / expired OAuth token
* Missing Ads permission
* Invalid music ID
* Geo-restriction (403)

Each failure is:

* Interpreted
* Explained clearly
* Accompanied by a suggested next step

---

## How to Run the Agent

### 1. Clone the repository

```bash
git clone <repo-url>
cd tiktok-ads-ai-agent
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Gemini API key

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the agent

```bash
python main.py
```

The agent will guide you through ad creation via the terminal.

---

## What This Project Demonstrates

* Strong prompt design
* Clear separation of concerns
* Correct business rule enforcement
* Sensible handling of unreliable APIs
* Practical engineering judgment
* Production-style AI workflow design

---

## What Is Not Included (By Design)

* Model fine-tuning
* Vector databases
* Multi-agent orchestration
* UI / frontend
* Production scaling

---



