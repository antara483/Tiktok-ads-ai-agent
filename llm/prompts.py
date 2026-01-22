SYSTEM_PROMPT = """
You are an AI assistant that creates TikTok Ad payloads.

RULES:
- Output ONLY valid JSON
- Do NOT add extra text
- Do NOT invent values
- Follow TikTok Ads rules strictly
"""

def build_payload_prompt(data: dict) -> str:
    return f"""
{SYSTEM_PROMPT}

Input:
Campaign Name: {data["campaign_name"]}
Objective: {data["objective"]}
Ad Text: {data["ad_text"]}
CTA: {data["cta"]}
Music ID: {data["music_id"]}

Return JSON in this format:
{{
  "campaign_name": "...",
  "objective": "...",
  "creative": {{
    "text": "...",
    "cta": "...",
    "music_id": "..."
  }}
}}
"""
