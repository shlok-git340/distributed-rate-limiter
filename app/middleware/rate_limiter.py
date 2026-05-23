import time

from flask import request, jsonify, g

from app.utils.identifiers import get_identifier
from app.algorithms.strategy_factory import get_rate_limiter
from app.metrics.prometheus_metrics import (
    REQUEST_COUNTER,
    BLOCKED_COUNTER,
    REQUEST_LATENCY
)

def register_rate_limiter(app):

    @app.before_request
    def rate_limit():

        start = time.time()

        identifier = get_identifier(request)

        limiter = get_rate_limiter()

        allowed = limiter.allow_request(
            identifier=identifier,
            route=request.path
        )

        latency = time.time() - start

        REQUEST_LATENCY.observe(latency)

        REQUEST_COUNTER.inc()

        if not allowed:

            BLOCKED_COUNTER.inc()

            return jsonify({
                "error": "Too Many Requests"
            }), 429