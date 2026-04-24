from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/ping", methods=["GET"])
@jwt_required(optional=True)
def ping_notifications():
    return jsonify({"status": "ok"})
