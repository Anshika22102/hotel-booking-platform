# app/models.py
from app import db
from datetime import datetime

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    rooms = db.relationship('Room', backref='hotel', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'city': self.city}

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='room', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'hotel_id': self.hotel_id, 'room_type': self.room_type, 'price': self.price, 'is_available': self.is_available}

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    guest_name = db.Column(db.String(100), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'room_id': self.room_id, 'guest_name': self.guest_name, 'check_in': self.check_in.isoformat(), 'check_out': self.check_out.isoformat(), 'total_price': self.total_price}

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_amount = db.Column(db.Float, nullable=False)
    one_time = db.Column(db.Boolean, default=True)
    max_usage = db.Column(db.Integer, default=1)
    usage_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {'id': self.id, 'code': self.code, 'discount_amount': self.discount_amount, 'one_time': self.one_time, 'max_usage': self.max_usage, 'usage_count': self.usage_count}

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
