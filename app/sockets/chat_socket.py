from flask import request
from flask_jwt_extended import decode_token
from flask_socketio import disconnect, emit


def register_chat(socketio):
    @socketio.on("connect")
    def auth_socket(auth=None):
        token = None
        if auth and isinstance(auth, dict):
            token = auth.get("token")
        if not token:
            token = request.args.get("token")
        if not token:
            return
        try:
            decode_token(token)
        except Exception:
            disconnect()

    @socketio.on("send_message")
    def handle_message(data):
        text = data.get("text") or data.get("message") or ""
        emit("receive_message", {"text": text}, broadcast=True)
