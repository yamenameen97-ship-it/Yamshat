import os
from flask import Blueprint, current_app, g, jsonify, redirect, render_template, request, session, url_for
from flask_jwt_extended import jwt_required
from app.utils.security import allowed_file, safe_filename

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@posts_bp.route("/web-login", methods=["POST"])
def web_login():
    username = request.form.get("username", "").strip()
    if username:
        session["user"] = username
        return redirect(url_for("home"))
    return redirect(url_for("posts.login_page"))


@posts_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("posts.login_page"))


@posts_bp.route("/post", methods=["POST"])
def create_post():
    content = request.form.get("content", "").strip()
    file = request.files.get("file")
    filename = ""

    if file and file.filename:
        if not allowed_file(file.filename):
            return jsonify({"error": "نوع الملف غير مدعوم"}), 400
        filename = safe_filename(file.filename)
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

    g.db.execute("INSERT INTO posts (content, media) VALUES (?, ?)", (content, filename))
    g.db.commit()
    return redirect(url_for("home"))


@posts_bp.route("/api/posts", methods=["GET"])
@jwt_required()
def get_posts():
    posts = g.db.execute("SELECT id, content, media FROM posts ORDER BY id DESC").fetchall()
    return jsonify([
        {"id": p["id"], "content": p["content"], "media": p["media"]}
        for p in posts
    ])
