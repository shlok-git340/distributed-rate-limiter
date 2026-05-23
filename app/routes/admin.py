from flask import Blueprint, request

from app.config.runtime_config import CONFIG

admin = Blueprint("admin", __name__)

@admin.route("/admin/config", methods=["POST"])
def update_config():

    data = request.json

    CONFIG["algorithm"] = data.get(
        "algorithm",
        CONFIG["algorithm"]
    )

    CONFIG["limit"] = data.get(
        "limit",
        CONFIG["limit"]
    )

    CONFIG["window"] = data.get(
        "window",
        CONFIG["window"]
    )

    return {
        "message": "Config updated",
        "config": CONFIG
    }