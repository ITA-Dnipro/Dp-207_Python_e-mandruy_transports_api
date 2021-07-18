import json
import jwt
import os
from klein import Response
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    DecodeError
)
from dotenv import load_dotenv

load_dotenv()


def is_valid_jwt_token(token):
    '''
    Check if jwt token is valid
    '''
    TRANSPORT_APP_JWT_SECRET = os.environ.get('TRANSPORT_APP_JWT_SECRET')
    try:
        jwt.decode(
            token,
            TRANSPORT_APP_JWT_SECRET,
            algorithms=["HS256"]
        )
        return True
    except (
            InvalidSignatureError,
            ExpiredSignatureError,
            DecodeError
            ) as err:
        response = {'error': err.args[0], 'code': 401}
        return response


def jwt_error_response(response):
    '''
    Return Klein Response with jwt error
    '''
    response = json.dumps(response)
    response = Response(
        headers={'Content-Type': 'application/json'},
        body=response.encode(),
        code=401
    )
    return response


if __name__ == "__main__":
    pass
