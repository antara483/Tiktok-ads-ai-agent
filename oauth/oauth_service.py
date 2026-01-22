

import time
import random

# Simulated in-memory token store
TOKEN_STORE = {}


def connect_tiktok():
    print("Redirecting user to TikTok OAuth...\n")

    # STEP 1: Authorization Code
    auth_code = generate_auth_code()
    print(f"🔐 Authorization code received: {auth_code}")

    # STEP 2: Exchange code for token
    token_response = exchange_code_for_token(auth_code)

    if "error" in token_response:
        explain_oauth_error(token_response["error"])
        return None

    access_token = token_response["access_token"]
    print("✅ TikTok connected successfully.\n")

    return access_token


def generate_auth_code():
    return f"auth_{random.randint(1000,9999)}"


def exchange_code_for_token(code):
    # Simulate failure cases
    if code.startswith("invalid"):
        return {"error": "invalid_client"}

    token = f"token_{random.randint(10000,99999)}"
    TOKEN_STORE[token] = {
        "expires_at": time.time() + 60,  # 1 min expiry
        "scope": "ads"
    }
    return {"access_token": token}


def explain_oauth_error(error):
    if error == "invalid_client":
        print("❌ Invalid client ID or secret.")
        print("👉 Check TikTok developer credentials.")
