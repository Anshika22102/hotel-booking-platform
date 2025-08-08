# app/routes/hotel_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import Hotel, Room

hotel_bp = Blueprint('hotel_bp', __name__)

def keyword_to_city(keyword):
    keyword = keyword.lower()
    mapping = {
        'tajmahal': 'agra',
        'redfort': 'delhi',
        'gateway': 'mumbai',
        'beach': 'goa',
        'agra': 'agra'
    }
    return mapping.get(keyword, keyword)

@hotel_bp.route('/', methods=['POST'])
def create_hotel():
    data = request.get_json() or {}
    name = data.get('name')
    city = data.get('city')
    if not name or not city:
        return jsonify({'error': 'Name and city required'}), 400
    hotel = Hotel(name=name, city=city)
    db.session.add(hotel)
    db.session.commit()
    return jsonify({'message': 'Hotel created', 'id': hotel.id}), 201

@hotel_bp.route('/<int:hotel_id>/rooms', methods=['POST'])
def add_room(hotel_id):
    data = request.get_json() or {}
    room_type = data.get('room_type')
    price = data.get('price')
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({'error': 'Hotel not found'}), 404
    room = Room(hotel_id=hotel_id, room_type=room_type, price=price)
    db.session.add(room)
    db.session.commit()
    return jsonify({'message': 'Room added', 'room_id': room.id}), 201

@hotel_bp.route('/search', methods=['GET'])
def search_hotels():
    name = request.args.get('name')
    city = request.args.get('city')
    keyword = request.args.get('keyword')
    query = Hotel.query
    if name:
        query = query.filter(Hotel.name.ilike(f"%{name}%"))
    if city:
        query = query.filter(Hotel.city.ilike(f"%{city}%"))
    if keyword:
        city_keyword = keyword_to_city(keyword)
        query = query.filter(Hotel.city.ilike(f"%{city_keyword}%"))
    hotels = query.all()
    return jsonify([h.to_dict() for h in hotels])
