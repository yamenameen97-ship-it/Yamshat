import os
import sqlite3
from flask import Flask, g, redirect, render_template, session, url_for
from config import Config
from .extensions import bcrypt, cors, jwt, limiter, talisman, socketio
from .routes.auth import auth_bp
from .routes.posts import posts_bp
from .routes.chat import chat_bp
from .routes.notifications import notifications_bp
from .sockets.chat_socket import register_chat
from .sockets.notify_socket import register_notify


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    talisman.init_app(app, content_security_policy=None)
    socketio.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(posts_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")

    register_chat(socketio)
    register_notify(socketio)

    @app.before_request
    def before_request():
        g.db = sqlite3.connect(app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row

    @app.teardown_request
    def teardown_request(exception=None):
        db = getattr(g, "db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def home():
        if "user" not in session:
            return redirect(url_for("posts.login_page"))
        posts = g.db.execute(
            "SELECT id, content, media FROM posts ORDER BY id DESC"
        ).fetchall()
        return render_template("feed.html", posts=posts)

    @app.route("/reels")
    def reels_page():
        return render_template("reels.html")

    @app.route("/stories")
    def stories_page():
        return render_template("stories.html")

    @app.route("/live")
    def live_page():
        return render_template("live.html")

    @app.route("/chat")
    def chat_page():
        return render_template("chat.html")

    @app.route("/market")
    def market_page():
        return render_template("market.html")

    @app.route("/profile")
    def profile_page():
        return render_template("profile.html")

    @app.route("/settings")
    def settings_page():
        return render_template("settings.html")

    return app
