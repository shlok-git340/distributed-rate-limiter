from flask import request, jsonify, g

from app.utils.identifiers import get_identifier
from app.algorithms.strategy_factory import get_rate_limiter


def register_rate_limiter(app):

    @app.before_request
    def rate_limit():
        if request.path.startswith("/admin"):
            return

        identifier = get_identifier(request)

        limiter = get_rate_limiter()

        allowed = limiter.allow_request(
            identifier=identifier,
            route=request.path
        )

        if not allowed:

            return jsonify({
                "error": "Too Many Requests"
            }), 429