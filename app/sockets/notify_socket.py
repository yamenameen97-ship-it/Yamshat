from flask_socketio import emit


def register_notify(socketio):
    @socketio.on("notify")
    def send_notify(data):
        user_id = data.get("user_id")
        if user_id:
            emit("notification", data, room=str(user_id))
        else:
            emit("new_notification", data, broadcast=True)
