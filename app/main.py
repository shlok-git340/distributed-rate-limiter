from flask import Flask

from app.routes.api import api
from app.routes.admin import admin

from app.middleware.auth import register_auth
from app.middleware.rate_limiter import (
    register_rate_limiter
)

app = Flask(__name__)

app.register_blueprint(api)
app.register_blueprint(admin)

register_auth(app)
register_rate_limiter(app)

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )