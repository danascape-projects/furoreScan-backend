import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import qrcode
from fpdf import FPDF
import os

# Encryption key (must be 16, 24, or 32 bytes long)
encryption_key = b'ada7327441e9876aaa5f19d8262c9482'[:16]  # Ensure it's 16 bytes for AES-128

# Fixed IV for example purposes (should be 16 bytes)
iv = b'1234567890123456'

def encrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + encrypted_data).decode('utf-8')

def generate_qr_code(data, file_path, size_cm=3):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    size_px = int(size_cm / 2.54 * 300)  # Convert cm to inches and multiply by DPI (300)
    img = img.resize((size_px, size_px))

    img.save(file_path)

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'QR Codes for Encrypted JSON Data', 0, 1, 'C')

json_list = []

# Loop to create JSON entries, encrypt, generate QR code, and add to PDF
for i in range(2001, 4001):
    id_str = str(i).zfill(4)
    json_data = json.dumps({
        "ID": id_str,
        "day1": "false",
        "day2": "false"
    })
    json_list.append(json_data)  # Add JSON data to the list
    json_str = json.dumps(json_data)
    encrypted_data = encrypt(json_data, encryption_key, iv)
    qr_code_path = f'qr_{id_str}.png'
    generate_qr_code(encrypted_data, qr_code_path)
    
    # Add QR code to PDF
    pdf.add_page()
    pdf.image(qr_code_path, x=60, y=60, w=30, h=30)
    pdf.set_y(160)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'ID: {id_str}', 0, 1, 'C')

    os.remove(qr_code_path)

# Save PDF to file
pdf_path = "encrypted_qrs2.pdf"
pdf.output(pdf_path)

# Save JSON list to file
json_list_path = "json_list2.json"
with open(json_list_path, 'w') as json_file:
    json.dump(json_list, json_file, indent=4)

print(f"PDF saved to {pdf_path}")
print(f"JSON list saved to {json_list_path}")
