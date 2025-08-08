# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import threading, time
from datetime import datetime, timedelta

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_booking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CHECKOUT_RELEASE_DELAY_MINUTES'] = 60  # how long after checkout to mark available

    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.routes.hotel_routes import hotel_bp
    from app.routes.booking_routes import booking_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(hotel_bp, url_prefix='/hotels')
    app.register_blueprint(booking_bp, url_prefix='/bookings')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Start background thread to release rooms after checkout time
    def background_release():
        with app.app_context():
            from app.models import Room, Booking
            while True:
                try:
                    now = datetime.utcnow()
                    # find bookings that ended before now
                    ended = Booking.query.filter(Booking.check_out <= now).all()
                    for b in ended:
                        room = b.room
                        # if no future bookings overlapping, mark available
                        future = Booking.query.filter(Booking.room_id==room.id, Booking.check_in > now).first()
                        if not future:
                            room.is_available = True
                            db.session.add(room)
                    db.session.commit()
                except Exception:
                    db.session.rollback()
                time.sleep(60)  # run every minute

    t = threading.Thread(target=background_release, daemon=True)
    t.start()

    return app
