import json

def generate_attendees(start: int, end: int):
    attendees = {}
    for i in range(start, end + 1):
        attendee_id = f"{i:04}"  # Format the number as a 4-digit string
        attendees[attendee_id] = {"day1": False, "day2": False}
    return attendees

def save_to_file(filename: str, data: dict):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

# Generate attendees from 0001 to 5000
attendees = generate_attendees(1, 5000)

# Save the attendees to a JSON file
save_to_file("attendees1.json", attendees)

