from datetime import datetime
from threading import Lock

# -----------------------------
# Models for Hotel, Room, Booking
# -----------------------------
class Hotel:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)


class Room:
    def __init__(self, hotel, room_type, price):
        self.hotel = hotel
        self.room_type = room_type
        self.price = price
        self.bookings = []
        self.lock = Lock()  # Lock to prevent double bookings
        hotel.add_room(self)

    def is_available(self, start_date, end_date):
        for booking in self.bookings:
            if not (end_date <= booking.start_date or start_date >= booking.end_date):
                return False
        return True

    def book(self, start_date, end_date):
        with self.lock:  # Prevent race condition
            if self.is_available(start_date, end_date):
                booking = Booking(self, start_date, end_date)
                self.bookings.append(booking)
                return booking
            else:
                return None


class Booking:
    def __init__(self, room, start_date, end_date):
        self.room = room
        self.start_date = start_date
        self.end_date = end_date


# -----------------------------
# Search Functionality
# -----------------------------
def search_hotels(hotels, city=None, name=None):
    result = hotels
    if city:
        result = [hotel for hotel in result if hotel.city.lower() == city.lower()]
    if name:
        result = [hotel for hotel in result if hotel.name.lower() == name.lower()]
    return result


# -----------------------------
# Generate Mock Data (1M Hotels)
# -----------------------------
def generate_mock_hotels(n=1000000):
    hotels = []
    for i in range(n):
        city = f"City{i % 100}"  # simulate 100 different cities
        name = f"Hotel{i}"
        hotel = Hotel(name, city)
        Room(hotel, room_type="Single", price=100 + i % 500)
        hotels.append(hotel)
    return hotels


# -----------------------------
# Utility to Parse Dates
# -----------------------------
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


# -----------------------------
# Test Cases
# -----------------------------
def test_simultaneous_booking():
    hotel = Hotel("Oceanview", "Goa")
    room = Room(hotel, "Single", 1000)

    start1 = parse_date("2025-08-02")
    end1 = parse_date("2025-08-04")
    booking1 = room.book(start1, end1)

    start2 = parse_date("2025-08-03")  # Overlaps
    end2 = parse_date("2025-08-04")
    booking2 = room.book(start2, end2)

    assert booking1 is not None, "Booking 1 should succeed"
    assert booking2 is None, "Booking 2 should fail due to overlap"
    print("Test Simultaneous Booking Passed")


def test_booking_edge_case():
    hotel = Hotel("EdgeHotel", "Delhi")
    room = Room(hotel, "Double", 1500)

    start = parse_date("2025-08-05")
    end = parse_date("2025-08-05")
    booking = room.book(start, end)

    assert booking is not None, "Booking with same check-in/check-out should succeed"
    print("Test Booking Edge Case Passed")


def test_search():
    hotel1 = Hotel("Oceanview", "Goa")
    hotel2 = Hotel("Mountain Inn", "Shimla")
    hotels = [hotel1, hotel2]

    result_city = search_hotels(hotels, city="Goa")
    result_name = search_hotels(hotels, name="Oceanview")

    assert len(result_city) == 1, "Search by city should return 1 result"
    assert len(result_name) == 1, "Search by name should return 1 result"
    print("Test Search Passed")


# -----------------------------
# Run All Tests
# -----------------------------
if __name__ == "__main__":
    test_simultaneous_booking()
    test_booking_edge_case()
    test_search()
    # Performance test (optional): uncomment to test
    # hotels = generate_mock_hotels(1000000)
    # print("Search result for City42:", len(search_hotels(hotels, city="City42")))
