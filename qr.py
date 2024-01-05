import json
import qrcode

def generate_qrcode(data, output_folder="qrcodes"):
    for attendee_id, details in data.items():
        # Create a QR code for the attendee ID
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(attendee_id)
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
