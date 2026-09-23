import random
import time
from datetime import datetime, timedelta
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
class Room:
    def __init__(self, number, room_type, price):
        self.number = number
        self.room_type = room_type
        self.price = price
        self.status = "Available"
class Reservation:
    def __init__(self, booking_id, customer, room, days):
        self.booking_id = booking_id
        self.customer = customer
        self.room = room
        self.days = days
        self.status = "Reserved"
        self.reservation_time = time.ctime()
        self.checkin_time = ""
        self.checkout_time = ""
        self.bill = 0
class Hotel:
    def __init__(self):
        self.rooms = []
        self.reservations = {}
        self.history = []
        self.customers = []
        self.create_rooms()
    def create_rooms(self):
        types = [("Single", 1000), ("Double", 1800),
                 ("Deluxe", 3000), ("Suite", 5000)]
        number = 101
        for room_type, price in types:
            for i in range(3):
                self.rooms.append(Room(number, room_type, price))
                number += 1
    def get_number(self, message):
        while True:
            try:
                n = int(input(message))
                if n > 0:
                    return n
                print("Enter a positive number.")
            except ValueError:
                print("Enter a valid number.")
    def generate_id(self):
        while True:
            booking_id = "HT" + str(random.randint(10000, 99999))
            if booking_id not in self.reservations:
                return booking_id
    def book_room(self):
        name = input("Customer name: ")
        phone = input("Phone number: ")
        print("1. Single  2. Double  3. Deluxe  4. Suite")
        choice = input("Room type: ")
        types = {"1": "Single", "2": "Double",
                 "3": "Deluxe", "4": "Suite"}
        if choice not in types:
            print("Invalid room type.")
            return
        days = self.get_number("Number of days: ")
        room_type = types[choice]
        room = next((r for r in self.rooms
                     if r.room_type == room_type
                     and r.status == "Available"), None)
        if room is None:
            print("No available room.")
            return
        customer = Customer(name, phone)
        self.customers.append(customer)
        booking_id = self.generate_id()
        reservation = Reservation(booking_id, customer, room, days)
        room.status = "Reserved"
        self.reservations[booking_id] = reservation
        print("Booking successful. ID:", booking_id)
    def check_in(self):
        booking_id = input("Booking ID: ").upper()
        r = self.reservations.get(booking_id)
        if r is None or r.status != "Reserved":
            print("Invalid booking.")
            return
        r.status = "Checked-In"
        r.checkin_time = time.ctime()
        r.room.status = "Checked-In"
        print("Check-in successful.")
    def calculate_bill(self, r):
        base = r.room.price * r.days
        weekend = 0
        start = datetime.now()
        for i in range(r.days):
            date = start + timedelta(days=i)
            if date.weekday() >= 5:
                weekend += r.room.price * 0.10
        discount = 0
        if r.days > 5:
            discount = (base + weekend) * 0.10
        return round(base + weekend - discount, 2)
    def check_out(self):
        booking_id = input("Booking ID: ").upper()
        r = self.reservations.get(booking_id)
        if r is None or r.status != "Checked-In":
            print("Invalid booking.")
            return
        r.status = "Checked-Out"
        r.checkout_time = time.ctime()
        late_charge = 500 if datetime.now().hour > 12 else 0
        r.bill = self.calculate_bill(r) + late_charge
        r.room.status = "Available"
        self.history.append({
            "booking_id": booking_id,
            "customer": r.customer.name,
            "bill": r.bill,
            "time": r.checkout_time
        })
        print("Total bill: ₹", r.bill)
    def cancel_booking(self):
        booking_id = input("Booking ID: ").upper()
        r = self.reservations.get(booking_id)
        if r is None or r.status in ["Cancelled", "Checked-Out"]:
            print("Invalid booking.")
            return
        days = self.get_number("Days before check-in: ")
        rate = 0 if days >= 7 else 0.25 if days >= 3 else 0.50
        r.bill = round(self.calculate_bill(r) * rate, 2)
        r.status = "Cancelled"
        r.room.status = "Available"
        self.history.append({
            "booking_id": booking_id,
            "cancellation_charge": r.bill
        })
        print("Cancelled. Charge: ₹", r.bill)
    def search_booking(self):
        booking_id = input("Booking ID: ").upper()
        r = self.reservations.get(booking_id)
        if r is None:
            print("Booking not found.")
            return
        print("Customer:", r.customer.name)
        print("Room:", r.room.number, r.room.room_type)
        print("Days:", r.days)
        print("Status:", r.status)
        print("Reservation time:", r.reservation_time)
    def show_history(self):
        for item in self.history:
            print(item)
    def show_rooms(self):
        for r in self.rooms:
            print(r.number, r.room_type, r.price, r.status)
    def menu(self):
        while True:
            print("\n1.Add Customer 2.Book Room 3.Check In")
            print("4.Check Out 5.Cancel 6.Search 7.History")
            print("8.Rooms 9.Exit")
            choice = input("Choice: ")
            if choice == "1":
                name = input("Name: ")
                phone = input("Phone: ")
                self.customers.append(Customer(name, phone))
                print("Customer added.")
            elif choice == "2":
                self.book_room()
            elif choice == "3":
                self.check_in()
            elif choice == "4":
                self.check_out()
            elif choice == "5":
                self.cancel_booking()
            elif choice == "6":
                self.search_booking()
            elif choice == "7":
                self.show_history()
            elif choice == "8":
                self.show_rooms()
            elif choice == "9":
                break
            else:
                print("Invalid choice.")
hotel = Hotel()
hotel.menu()

