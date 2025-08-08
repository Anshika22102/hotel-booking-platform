# app/routes/booking_routes.py
from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Hotel, Room, Booking, Coupon
from datetime import datetime
from sqlalchemy import and_, or_

booking_bp = Blueprint('booking_bp', __name__)

def overlaps(room_id, start_dt, end_dt):
    # returns True if any booking overlaps given period for room
    q = Booking.query.filter(Booking.room_id == room_id).filter(
        or_(
            and_(Booking.check_in <= start_dt, Booking.check_out > start_dt),
            and_(Booking.check_in < end_dt, Booking.check_out >= end_dt),
            and_(Booking.check_in >= start_dt, Booking.check_out <= end_dt)
        )
    )
    return db.session.query(q.exists()).scalar()

@booking_bp.route('/book', methods=['POST'])
def book_room():
    data = request.get_json() or {}
    room_id = data.get('room_id')
    guest_name = data.get('guest_name')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    coupon_code = data.get('coupon_code')

    if not all([room_id, guest_name, check_in, check_out]):
        return jsonify({'error': 'room_id, guest_name, check_in, check_out required'}), 400

    try:
        start_dt = datetime.fromisoformat(check_in)
        end_dt = datetime.fromisoformat(check_out)
    except Exception as e:
        return jsonify({'error': 'Invalid date format. Use ISO format.'}), 400

    if start_dt > end_dt:
        return jsonify({'error': 'check_in must be before check_out'}), 400

    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404

    # check overlap
    if overlaps(room_id, start_dt, end_dt):
        return jsonify({'error': 'Room already booked for the selected dates'}), 409

    # compute price (simple: days * price)
    nights = (end_dt.date() - start_dt.date()).days or 1
    total = nights * room.price

    # apply coupon if provided
    applied_coupon = None
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code).first()
        if coupon and coupon.usage_count < coupon.max_usage:
            total = max(0, total - coupon.discount_amount)
            coupon.usage_count += 1
            applied_coupon = coupon.code
            db.session.add(coupon)

    # create booking within transaction
    try:
        booking = Booking(room_id=room_id, guest_name=guest_name, check_in=start_dt, check_out=end_dt, total_price=total)
        room.is_available = False
        db.session.add(booking)
        db.session.add(room)
        db.session.commit()
        return jsonify({'message': 'Booking confirmed', 'booking': booking.to_dict(), 'coupon_applied': applied_coupon}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Booking failed', 'details': str(e)}), 500

@booking_bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    b = Booking.query.get(booking_id)
    if not b:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(b.to_dict())
