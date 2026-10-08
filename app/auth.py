import os
from functools import wraps

from flask import request


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        expected = os.getenv("API_KEY", "my-secret-api-key-123")
        if not api_key or api_key != expected:
            return {"message": "Unauthorized. Provide valid X-API-KEY header."}, 401
        return f(*args, **kwargs)

    return decorated
