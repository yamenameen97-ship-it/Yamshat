from flask import Blueprint, g, jsonify, request, session
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.extensions import bcrypt, limiter

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("10 per minute")
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "username et password requis"}), 400

    existing = g.db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    if existing:
        return jsonify({"error": "اسم المستخدم مستخدم بالفعل"}), 409

    hashed = bcrypt.generate_password_hash(password).decode("utf-8")
    g.db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
    g.db.commit()
    return jsonify({"msg": "تم التسجيل"})


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("20 per minute")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    user = g.db.execute("SELECT id, username, password FROM users WHERE username=?", (username,)).fetchone()

    if user and bcrypt.check_password_hash(user["password"], password):
        access = create_access_token(identity=str(user["id"]))
        refresh = create_refresh_token(identity=str(user["id"]))
        session["user"] = user["username"]
        return jsonify({
            "access_token": access,
            "refresh_token": refresh,
            "username": user["username"]
        })

    return jsonify({"error": "بيانات خاطئة"}), 401


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_token})
