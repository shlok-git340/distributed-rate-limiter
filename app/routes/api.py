from flask import Blueprint

api = Blueprint("api", __name__)

@api.route("/unlimited")
def unlimited():

    return {
        "message": "Unlimited access"
    }

@api.route("/limited")
def limited():

    return {
        "message": "Protected endpoint"
    }