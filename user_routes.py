from flask import Blueprint, request, jsonify
from extensions import db
from models import User

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.post("/me/avatar")
def set_avatar():
    data = request.get_json(silent=True) or {}
    secure_url = data.get("secure_url")
    user_id = int(data.get("user_id") or 1)

    if not secure_url:
        return jsonify(error="secure_url required"), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify(error="user not found"), 404

    user.avatar_url = secure_url
    db.session.commit()
    return jsonify(ok=True, avatar_url=user.avatar_url), 200
