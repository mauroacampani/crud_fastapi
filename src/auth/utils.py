from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import Config
import uuid
import logging
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from typing import Union
from itsdangerous import URLSafeSerializer, SignatureExpired, BadSignature, URLSafeTimedSerializer
from fastapi import HTTPException

passwd_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload= {}

    payload['user'] = user_data
    payload['exp'] = datetime.utcnow() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token:str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=  token,
            key=Config.JWT_SECRET,
            algorithms= [Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

# def decode_token(token: str) -> Union[dict, None]:
#     try:
#         token_data = jwt.decode(
#             jwt=token,
#             key=Config.JWT_SECRET,
#             algorithms=[Config.JWT_ALGORITHM]
#         )
#         return token_data
#     except ExpiredSignatureError:
#         logging.warning("Token expirado")
#         return None
#     except InvalidTokenError as e:
#         logging.warning(f"Token inválido: {e}")
#         return None


serializer = URLSafeTimedSerializer(
        secret_key=Config.JWT_SECRET,
        salt="email-configuration"
    )


def create_url_safe_token(data: dict) -> str:

    token = serializer.dumps(data, salt="email-configuration")

    return token


def decode_url_safe_token(token: str, max_age: int = 3600):

    try:

        token_data = serializer.loads(token, salt="email-configuration", max_age=max_age)

        return token_data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")