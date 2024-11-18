from services.token_admin import get_token_from_headers
from utils.token_generator import verify_access_token, verify_refresh_token


def authenticate(request):
    try:
        headers = request.headers
        token = get_token_from_headers(headers)

        if token:
            decoded = verify_access_token(token)
            if decoded:
                user = decoded.get("user")
                return user
            else:
                return None
        else:
            return None

    except Exception as e:
        return {"error": str(e)}
