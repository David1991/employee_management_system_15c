from odoo.http import request
import jwt
from odoo.tools import config

JWT_SECRET = config.get('jwt_secret')
JWT_ALGORITHM = "HS256"

def authenticate_jwt():
    authorization = request.httprequest.headers.get("Authorization")

    if not authorization:
        return {
            "status" : False,
            "message" : "Authorization Header is missing!",
        }
    
    try:
        # Remove Bearer prefix
        token = authorization.replace("Bearer ", "")

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        return payload

    except jwt.InvalidTokenError:
        return {
            "status": False,
            "message": "Invalid token!"
        }
    # return authorization