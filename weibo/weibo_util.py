from util import list_util, number_util, date_util


MBLOG_DATE_PATTERN = "%a %b %d %H:%M:%S %z %Y"


def find_card_nine(card: dict):
    if card["card_type"] == 9:
        return card
    if "card_group" in card and list_util.is_not_empty(card["card_group"]):
        return find_card_nine(card["card_group"][0])
    return None


def process_mblog(card: dict):
    mblog = card["mblog"]
    user = mblog["user"]
    return {
        "mid": mblog["mid"],
        "original_text": mblog["text"],
        "like_count": number_util.to_number(mblog["attitudes_count"]),
        "comment_count": number_util.to_number(mblog["comments_count"]),
        "repost_count": number_util.to_number(mblog["reposts_count"]),
        "pictures": [
            item["url"] for item in mblog["pics"]
        ] if "pics" in mblog and list_util.is_not_empty(mblog["pics"]) else [],
        "user": {
            "user_id": user["id"],
            "username": user["screen_name"],
            "description": user["description"],
            "gender": user["gender"],
            "profile_url": user["profile_url"],
            "profile_image": user["profile_image_url"],
            "verified": user["verified"],
            "verified_reason": user["verified_reason"],
            "follow_count": number_util.to_number(user["follow_count"]),
            "followers_count": number_util.to_number(user["followers_count"]),
        },
        "source_device": mblog["source"],
        "country": mblog.get("status_country"),
        "province": mblog.get("status_province"),
        "city": mblog.get("status_city"),
        "created_at": date_util.to_datetime(mblog["created_at"], MBLOG_DATE_PATTERN),
    }
