import time
import jwt

from app.config import SECRET_KEY, ALGORITHM


def generate_token(user_id, email):
    token_data = {
        'user_id': user_id,
        'email': email,
        'expire': time.time() + 3600    # 1時間
    }

    token = _jwt_encode(
        token_data,
        secret=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token.decode()


def decode_token(token):
    token_data = _jwt_decode(token, secret=SECRET_KEY)
    if token_data is None:
        raise Exception('invalid token')
    else:
        return token_data


def _jwt_encode(dict_data, secret, algorithm):
    return jwt.encode(dict_data, secret, algorithm=algorithm)


def _jwt_decode(encoded, secret):
    try:
        token = jwt.decode(encoded, secret)
    except jwt.exceptions.DecodeError as e:
        print(e)
        token = None

    return token
