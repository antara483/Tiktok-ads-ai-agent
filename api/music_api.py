def validate_music_id(music_id):
    # Mock validation logic
    if music_id == "invalid":
        return {
            "success": False,
            "error": "Music ID not approved for ads"
        }

    return {"success": True}
