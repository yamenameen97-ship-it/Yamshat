from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from flask_talisman import Talisman

bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
talisman = Talisman()
socketio = SocketIO(async_mode="eventlet")
