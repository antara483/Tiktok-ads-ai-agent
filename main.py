from agent.conversation import start_conversation
from oauth.oauth_service import connect_tiktok

def main():
    print("Welcome to TikTok Ads AI Agent\n")

    # Step 1: OAuth
    token = connect_tiktok()
    if not token:
        print("Failed to authenticate with TikTok.")
        return

    # Step 2: Conversation
    ad_payload = start_conversation(token)

    print("\n✅ Final Validated Ad Payload:")
    print(ad_payload)

if __name__ == "__main__":
    main()
