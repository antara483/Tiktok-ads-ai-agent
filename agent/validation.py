
from api.music_api import validate_music_id

def validate_music(objective):
    print("\nMusic Options:")
    print("1. Existing Music ID")
    print("2. Upload Custom Music")
    print("3. No Music")

    choice = input("Choose (1/2/3): ")

    if choice == "3":
        if objective == "Conversions":
            print("❌ Music required for Conversion campaigns.")
            return validate_music(objective)
        return None

    if choice == "1":
        music_id = input("Enter Music ID: ")
        result = validate_music_id(music_id)

        if not result["success"]:
            print(f"❌ {result['error']}")
            print("👉 Choose another music option.")
            return validate_music(objective)

        return music_id

    if choice == "2":
        print("Uploading music...")
        music_id = "mock_uploaded_music_123"
        return music_id
