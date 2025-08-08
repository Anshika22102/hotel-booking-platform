# run.py
from app import create_app, db
from app.models import Hotel, Room, Booking, Coupon, Manager

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
