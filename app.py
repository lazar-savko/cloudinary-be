import os
import cloudinary
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CLOUDINARY_CLOUD_NAME"] = os.environ["CLOUDINARY_CLOUD_NAME"]
    app.config["CLOUDINARY_API_KEY"] = os.environ["CLOUDINARY_API_KEY"]
    app.config["CLOUDINARY_API_SECRET"] = os.environ["CLOUDINARY_API_SECRET"]
    app.config["CLOUDINARY_AVATAR_PRESET"] = os.environ["CLOUDINARY_AVATAR_PRESET"]

    CORS(app, supports_credentials=True)
    db.init_app(app)

    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
        secure=True
    )

    # Import blueprints AFTER app/db are ready
    from media_routes import bp as media_bp
    from user_routes import bp as users_bp
    app.register_blueprint(media_bp)
    app.register_blueprint(users_bp)

    # Import models AFTER db.init_app(app), so tables can be created
    with app.app_context():
        from models import User
        db.create_all()
        if not User.query.filter_by(email="demo@example.com").first():
            db.session.add(User(email="demo@example.com"))
            db.session.commit()

    @app.get("/ping")
    def ping():
        return {"ok": True}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
