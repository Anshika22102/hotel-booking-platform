# Database Schema

## Hotel
- id (int, PK)
- name (string)
- city (string)

## Room
- id (int, PK)
- hotel_id (int, FK -> Hotel.id)
- room_type (string)
- price (float)
- is_available (bool)

## Booking
- id (int, PK)
- room_id (int, FK -> Room.id)
- guest_name (string)
- check_in (datetime)
- check_out (datetime)
- total_price (float)
- created_at (datetime)

## Coupon
- id (int, PK)
- code (string, unique)
- discount_amount (float)
- one_time (bool)
- max_usage (int)
- usage_count (int)

## Manager
- id (int, PK)
- name (string)
- email (string)
- hotel_id (int, FK -> Hotel.id)
