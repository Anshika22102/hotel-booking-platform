# app/routes/dashboard_routes.py
from flask import Blueprint, render_template, jsonify
from app.models import Hotel, Room, Booking
from app import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='templates')

@dashboard_bp.route('/manager/<int:hotel_id>', methods=['GET'])
def manager_dashboard(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return "Hotel not found", 404
    # ongoing bookings: bookings where check_out >= now
    from datetime import datetime
    now = datetime.utcnow()
    ongoing = Booking.query.join(Room).filter(Room.hotel_id==hotel_id, Booking.check_out >= now).all()
    revenue = db.session.query(func.sum(Booking.total_price)).join(Room).filter(Room.hotel_id==hotel_id).scalar() or 0.0
    return render_template('dashboard.html', hotel=hotel, ongoing=ongoing, revenue=revenue)

@dashboard_bp.route('/api/manager/<int:hotel_id>/stats', methods=['GET'])
def manager_stats(hotel_id):
    from datetime import datetime
    now = datetime.utcnow()
    ongoing_count = Booking.query.join(Room).filter(Room.hotel_id==hotel_id, Booking.check_out >= now).count()
    revenue = db.session.query(func.sum(Booking.total_price)).join(Room).filter(Room.hotel_id==hotel_id).scalar() or 0.0
    return jsonify({'ongoing_bookings': ongoing_count, 'revenue': revenue})
