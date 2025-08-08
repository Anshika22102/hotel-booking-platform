# 🏨 Hotel Room Booking Platform (Flask)

## 📁 Problem Statement

Build a full-stack hotel room booking system with the following features:

1. Create Hotels and Rooms with types, prices, and availability.
2. Book rooms for specific date ranges.
3. Prevent double bookings (overlapping dates).
4. Search hotels by city, name, or tourist keyword (e.g., “Tajmahal” → Agra).
5. Auto-release rooms after checkout time.
6. Dashboard for hotel managers to view ongoing bookings and revenue.
7. Apply discounts via 1-time or multiple-use coupons.
8. Document database schema.
9. Provide Postman collection for testing.

---

## 💡 My Approach

- **Framework**: Flask with SQLAlchemy ORM for persistence.
- **Models**: `Hotel`, `Room`, `Booking`, `Coupon`, and `Manager`.
- **Search**: Supports name, city, and keyword→city mapping.
- **Concurrency**: Prevents overlapping bookings at DB query level.
- **Coupons**: Best applicable coupon applied automatically (optional input).
- **Background Job**: Thread checks every minute to mark rooms as available after checkout.
- **Manager Dashboard**: HTML (Jinja2) template to show bookings and revenue in real-time.
- **Documentation**: Added `schema.md` and `postman_collection.json`.

---

## 🔧 Setup Instructions

### ✅ Prerequisites
- Python 3.8+
- pip
- Git

### 🔄 Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/hotel-booking-platform.git
cd hotel-booking-platform
```

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 🗄 Initialize Database
```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "init"
flask db upgrade
```

### ⚡ Run the Project
```bash
python run.py
```
The server will start at `http://127.0.0.1:5000`

---

## 📊 Postman Collection
Import `postman_collection.json` into Postman to test APIs:
- Create hotel
- Add room
- Search hotels
- Book room
- View dashboard stats

---

## 🧠 Complex Logic Explanation

### ✅ Booking Conflict Detection
Bookings are rejected if any existing booking overlaps with the requested check-in/out date range:
```python
if overlaps(room_id, start_dt, end_dt):
    return jsonify({'error': 'Room already booked'}), 409
```

### 🕒 Auto Room Release
A background thread runs every 60 seconds:
```python
if booking.check_out <= now and no future bookings:
    room.is_available = True
```

### 🔍 Smart Search
Keyword mapping for popular tourist spots:
```python
'tajmahal' → 'agra'
'redfort' → 'delhi'
'gateway' → 'mumbai'
'beach' → 'goa'
```

---

## 🖥 Manager Dashboard
Accessible at:
```
/dashboard/manager/<hotel_id>
```
Displays:
- Hotel details
- Ongoing bookings
- Total revenue

---

## 📂 Deliverables
- [x] Persistent DB (SQLite)
- [x] REST APIs with Flask
- [x] Improved search logic
- [x] Manager dashboard
- [x] Auto room availability
- [x] Coupon discounts
- [x] DB schema documentation
- [x] Postman collection

---

## 🎥 Loom Video Walkthrough
[🔗 Watch Video](https://www.loom.com/share/68a8cf69bde24bcbb1fefb4753b6c52c?sid=b1918cda-9c5e-447a-b20b-dd692476bf5e)

---

## 🏆 Author
Built with ❤️ by Anshika.
