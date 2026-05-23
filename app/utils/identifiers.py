from flask import g

def get_identifier(request):

    if g.get("user_id"):
        return f"user:{g.user_id}"

    return f"ip:{request.remote_addr}"