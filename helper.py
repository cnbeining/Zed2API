import jwt
import uuid
from datetime import datetime, timedelta

github_username_zed_userid_list = [
    ("aaa", 123123),
]

def create_jwt(github_user_login: str, user_id: int) -> str:
    LLM_TOKEN_LIFETIME = timedelta(hours=1)
    now = datetime.utcnow()

    payload = {
        "iat": int(now.timestamp()),
        "exp": int((now + LLM_TOKEN_LIFETIME).timestamp()),
        "jti": str(uuid.uuid4()),
        "userId": user_id,
        "githubUserLogin": github_user_login,
        "isStaff": False,
        "hasLlmClosedBetaFeatureFlag": False,
        "plan": "Free"
    }

    return jwt.encode(payload, 'llm-secret', algorithm='HS256')
