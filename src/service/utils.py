import logging
import uuid
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.service.config import Config

passwd_context = CryptContext(schemes=["bcrypt"])


def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {
        "user": user_data,
        "exp": datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return {}


# serializer = URLSafeTimedSerializer(
#     secret_key=Config.JWT_SECRET, salt="email-configuration"
# )
#
#
# def create_url_safe_token(data: dict):
#
#     token = serializer.dumps(data)
#
#     return token
#
#
# def decode_url_safe_token(token: str):
#     try:
#         token_data = serializer.loads(token)
#
#         return token_data
#
#     except Exception as e:
#         logging.error(str(e))
