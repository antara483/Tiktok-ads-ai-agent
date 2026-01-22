

import time
from oauth.oauth_service import TOKEN_STORE


def submit_ad(payload, token):
    print("\nSubmitting ad to TikTok Ads API...")

    # Token missing
    if token not in TOKEN_STORE:
        explain_api_error("invalid_token")
        return

    token_data = TOKEN_STORE[token]

    # Token expired
    if time.time() > token_data["expires_at"]:
        explain_api_error("expired_token")
        return

    # Missing permission
    if token_data["scope"] != "ads":
        explain_api_error("missing_scope")
        return

    # Invalid music
    if payload["creative"]["music_id"] == "invalid":
        explain_api_error("invalid_music")
        return

    print("✅ Ad submitted successfully!")


def explain_api_error(error):
    if error == "invalid_token":
        print("❌ OAuth token is invalid.")
        print("👉 Please reconnect TikTok Ads.")

    elif error == "expired_token":
        print("❌ OAuth token has expired.")
        print("👉 Re-authenticate to continue.")

    elif error == "missing_scope":
        print("❌ Missing Ads permission scope.")
        print("👉 Reauthorize with Ads permissions.")

    elif error == "invalid_music":
        print("❌ Music ID is invalid.")
        print("👉 Choose a different music track.")

    elif error == "geo_restricted":
        print("❌ TikTok Ads not available in your region.")
