# app/services/booking_service.py
from app.models import Booking, Room
from datetime import datetime
from app import db

def release_rooms_after_checkout():
    now = datetime.utcnow()
    ended = Booking.query.filter(Booking.check_out <= now).all()
    for b in ended:
        room = b.room
        future = Booking.query.filter(Booking.room_id==room.id, Booking.check_in > now).first()
        if not future:
            room.is_available = True
            db.session.add(room)
    db.session.commit()
