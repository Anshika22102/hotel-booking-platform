# Hotel Room Booking Platform

## Problem Statement

Build a hotel room booking system with the following features:

1. Create Hotels and Rooms with room types and prices.
2. Book rooms for specific date ranges.
3. Prevent double booking (overlapping date ranges).
4. Search hotels by city or name.
5. Demonstrate performance with 1M mock hotels.
6. Include test cases to validate behavior.

---

## My Approach

- Modeled `Hotel`, `Room`, and `Booking` using simple Python classes.
- Used `threading.Lock` to handle concurrency and prevent double bookings.
- Wrote in-memory search logic using efficient list filters.
- Simulated 1M hotel data using a loop for performance testing.
- Wrote 3 test cases:
  - Simultaneous room booking
  - Booking with same check-in/out date
  - Search hotels by city or name

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git (to clone the repo)

### Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/hotel-booking-platform.git
cd hotel-booking-platform
```

### Run the Project
```bash
python hotel_booking_platform.py
```

### Run Test Cases
Test cases run automatically when you execute the file.
Uncomment the mock data section to benchmark performance.

---

## Complex Logic Explanation

### Booking Conflict Detection
```python
def is_available(self, start_date, end_date):
    for booking in self.bookings:
        if not (end_date <= booking.start_date or start_date >= booking.end_date):
            return False
    return True
```

### Thread-Safety via Lock
```python
with self.lock:
    if self.is_available(...):
        # safe to book
```

---

## Loom Video Walkthrough

### [🔗 Click to Watch on Loom](https://www.loom.com/share/f28b0df885a941be8a8fba812dca1444?sid=c03b8c2a-ea4f-4ebe-b369-c19720f9cf7c)

---

## 🧾 Deliverables

- [x] Hotel and Room Models
- [x] Booking with Overlap Prevention
- [x] Search Function
- [x] Handle 1M Mock Hotels
- [x] 3 Test Cases
- [x] Code Comments
- [ ] Flask API (optional future work)
- [ ] UI / Dashboard (optional future work)

---

## 🏆 Author
Built with ❤️ by Anshika.
