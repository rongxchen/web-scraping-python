from common.const import HTTP_USER_AGENT


def get_header():
    return {
        "User-Agent": HTTP_USER_AGENT,
    }
