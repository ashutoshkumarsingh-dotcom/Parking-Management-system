import json
import math
import os

TOTAL_SLOTS = 5
DATA_FILE = "parking.txt"

# Five empty parking slots
slots = [None] * TOTAL_SLOTS


# Load saved parking data
def load_data():
    global slots

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            if isinstance(data, list) and len(data) == TOTAL_SLOTS:
                slots = data
        except (json.JSONDecodeError, OSError):
            print("Could not load saved data.")


# Save parking data
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(slots, file, indent=4)


# Validate vehicle number
def valid_number(number):
    return (
        number.isalnum()
        and 8 <= len(number) <= 12
    )


# Find vehicle in parking
def find_vehicle(number):
    for i, vehicle in enumerate(slots):
        if vehicle and vehicle["number"] == number:
            return i
    return -1


# Vehicle entry
def entry():
    number = input("Enter vehicle number: ").strip().upper()

    if not valid_number(number):
        print("Invalid vehicle number.")
        return

    if find_vehicle(number) != -1:
        print("Vehicle is already parked.")
        return

    vehicle_type = input("Enter type (car/bike): ").strip().lower()

    if vehicle_type not in ["car", "bike"]:
        print("Invalid type. Enter car or bike.")
        return

    for i in range(TOTAL_SLOTS):
        if slots[i] is None:
            slots[i] = {
                "number": number,
                "type": vehicle_type
            }

            save_data()

            print("Vehicle", number, "parked in slot", i + 1)
            print("Slots free:", slots.count(None))
            return

    print("Parking lot is full.")


# Calculate parking fee
def calculate_fee(vehicle_type, hours):
    charged_hours = max(1, math.ceil(hours))

    if vehicle_type == "car":
        rate = 20
    else:
        rate = 10

    fee = charged_hours * rate
    return charged_hours, fee


# Vehicle exit
def exit_vehicle():
    number = input("Enter vehicle number: ").strip().upper()

    index = find_vehicle(number)

    if index == -1:
        print("Vehicle", number, "not found.")
        return

    try:
        hours = float(input("Enter parking hours: "))

        if not math.isfinite(hours) or hours <= 0:
            print("Invalid parking hours.")
            return

    except ValueError:
        print("Please enter valid hours.")
        return

    vehicle = slots[index]

    charged_hours, fee = calculate_fee(
        vehicle["type"], hours
    )

    print("Hours charged:", charged_hours)
    print("Parking fee: Rs.", fee)

    slots[index] = None
    save_data()

    print("Slot", index + 1, "is now free.")


# Display parking status
def status():
    print("\n----- PARKING STATUS -----")

    for i, vehicle in enumerate(slots):
        if vehicle:
            print(
                "Slot", i + 1,
                ":", vehicle["number"],
                "-", vehicle["type"]
            )
        else:
            print("Slot", i + 1, ": Empty")

    print("Slots free:", slots.count(None), "of", TOTAL_SLOTS)


# Main program
load_data()

while True:
    print("\n===== PARKING MANAGEMENT SYSTEM =====")
    print("1. Entry")
    print("2. Exit")
    print("3. Status")
    print("4. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        entry()

    elif choice == "2":
        exit_vehicle()

    elif choice == "3":
        status()

    elif choice == "4":
        print("Thank you for using Parking Management System!")
        break

    else:
        print("Invalid choice. Try again.")