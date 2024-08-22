import jwt
import uuid
from datetime import datetime, timedelta
import random
import string

github_username_zed_userid_list = [
    ("aaa", 123123),
]


def generate_random_tuple():
    """
    Generate a random tuple containing a string and an integer.

    Returns:
        tuple: A tuple containing:
            - str: A random string of length 6-12 consisting of ASCII letters and digits.
            - int: A random 6-digit integer between 100000 and 999999.
    """
    # Generate a random string of length 6-12
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(6, 12)))
    
    # Generate a random 6-digit integer
    random_int = random.randint(100000, 999999)
    
    return (random_string, random_int)


def create_jwt(github_user_login: str, user_id: int) -> str:
    """
    Create a JSON Web Token (JWT) for a given GitHub user.

    Args:
        github_user_login (str): The GitHub username of the user.
        user_id (int): The user's ID.

    Returns:
        str: A JWT encoded string containing user information and authentication details.

    Note:
        The token has a lifetime of 1 hour and includes the following claims:
        - iat: Issued at time
        - exp: Expiration time
        - jti: Unique token identifier
        - userId: User's ID
        - githubUserLogin: GitHub username
        - isStaff: Boolean indicating staff status (default: False)
        - hasLlmClosedBetaFeatureFlag: Boolean for LLM closed beta feature (default: False)
        - plan: User's plan (default: "Free")
    """
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