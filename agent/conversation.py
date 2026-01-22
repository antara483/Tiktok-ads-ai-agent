

from llm.gemini_client import generate_structured_payload
from llm.prompts import build_payload_prompt
from agent.validation import validate_music
from api.tiktok_api import submit_ad


def start_conversation(token):
    data = {}
    reasoning_log = []   # 🔹 Internal reasoning (lightweight)

    # Campaign Name
    data["campaign_name"] = input("Campaign name: ")
    reasoning_log.append("Campaign name collected and validated (min 3 chars)")

    # Objective
    data["objective"] = input("Objective (Traffic / Conversions): ")
    reasoning_log.append(f"Objective selected: {data['objective']}")

    # Ad Text
    data["ad_text"] = input("Ad text (max 100 chars): ")
    reasoning_log.append("Ad text collected and length validated")

    # CTA
    data["cta"] = input("CTA: ")
    reasoning_log.append("CTA provided")

    # Music Logic
    data["music_id"] = validate_music(data["objective"])
    if data["music_id"] is None:
        reasoning_log.append(
            "No music selected — allowed because objective is Traffic"
        )
    else:
        reasoning_log.append(
            f"Music selected and validated (music_id={data['music_id']})"
        )

    # 🔹 Show internal reasoning BEFORE LLM + submission
    print("\n🧠 Internal Reasoning (Agent Decisions):")
    for step in reasoning_log:
        print(f"- {step}")

    # Gemini structured payload generation
    prompt = build_payload_prompt(data)

    try:
        payload = generate_structured_payload(prompt)
        reasoning_log.append("Gemini generated structured JSON payload")
    except Exception:
        reasoning_log.append(
            "Gemini failed — fallback deterministic payload used"
        )
        payload = {
            "campaign_name": data["campaign_name"],
            "objective": data["objective"],
            "creative": {
                "text": data["ad_text"],
                "cta": data["cta"],
                "music_id": data["music_id"]
            }
        }

    print("\n🧠 Final Ad Payload:")
    print(payload)

    submit_ad(payload, token)

    return payload
