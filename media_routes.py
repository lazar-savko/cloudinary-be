# media_routes.py
import time
from flask import Blueprint, request, jsonify, current_app
from cloudinary.utils import api_sign_request

bp = Blueprint("media", __name__, url_prefix="/media")

@bp.post("/signature")
def get_signature():
    body = request.get_json(silent=True) or {}
    user_id = str(body.get("user_id") or "1")

    params_to_sign = {
        "timestamp": int(time.time()),
        "folder": f"profiles/{user_id}/",
        "public_id": "avatar",
        "overwrite": "true",
        # note: no upload_preset here
        # if you want eager thumbs, sign them too:
        # "eager": "c_fill,w_256,h_256,g_auto",
    }

    signature = api_sign_request(params_to_sign, current_app.config["CLOUDINARY_API_SECRET"])

    return jsonify({
        "cloud_name": current_app.config["CLOUDINARY_CLOUD_NAME"],
        "api_key": current_app.config["CLOUDINARY_API_KEY"],
        "signature": signature,
        **params_to_sign
    }), 200
