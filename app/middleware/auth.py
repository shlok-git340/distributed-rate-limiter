import jwt

from flask import request, g
import os

SECRET = os.getenv(
    "JWT_SECRET",
    "super-secret"
)


def register_auth(app):

    @app.before_request
    def authenticate():

        token = request.headers.get("Authorization")

        if not token:
            g.user_id = None
            return

        try:

            token = token.split(" ")[1]

            payload = jwt.decode(
                token,
                SECRET,
                algorithms=["HS256"]
            )

            g.user_id = payload["user_id"]

        except Exception:
            g.user_id = None