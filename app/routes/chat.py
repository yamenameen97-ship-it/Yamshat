from flask import Blueprint, render_template

chat_bp = Blueprint("chat_routes", __name__)


@chat_bp.route("/chat-ui")
def chat_ui():
    return render_template("chat.html")
