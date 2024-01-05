import json
import qrcode

def generate_qrcode(data, output_folder="qrcodes"):
    for attendee_id, details in data.items():
        # Create a dictionary with only ID, day1, and day2
        qr_data = {"ID": attendee_id, "day1": details.get("day1", False), "day2": details.get("day2", False)}

        # Convert the dictionary to a string and create a QR code
        qr_data_str = json.dumps(qr_data, indent=2)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data_str)
        qr.make(fit=True)

        # Save the QR code as an image
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{output_folder}/{attendee_id}.png")

def main():
    # Load attendees from a JSON file
    try:
        with open("attendees.json", "r") as file:
            attendees_data = json.load(file)
    except FileNotFoundError:
        print("File 'attendees.json' not found.")
        return

    # Generate QR codes for each attendee
    generate_qrcode(attendees_data)

if __name__ == "__main__":
    main()
