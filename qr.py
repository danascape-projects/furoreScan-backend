import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import qrcode
from fpdf import FPDF

# Encryption key (must be 16, 24, or 32 bytes long)
encryption_key = b'ada7327441e9876aaa5f19d8262c9482'[:16]  # Ensure it's 16 bytes for AES-128

# Fixed IV for example purposes (should be 16 bytes)
iv = b'1234567890123456'

def encrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + encrypted_data).decode('utf-8')

def generate_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(file_path)

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'QR Codes for Encrypted JSON Data', 0, 1, 'C')

# Loop to create JSON entries, encrypt, generate QR code, and add to PDF
for i in range(1, 5001):
    id_str = str(i).zfill(4)
    json_data = json.dumps({id_str: {"day1": False, "day2": False}})
    encrypted_data = encrypt(json_data, encryption_key, iv)
    qr_code_path = f'qr_{id_str}.png'
    generate_qr_code(encrypted_data, qr_code_path)
    
    # Add QR code to PDF
    pdf.add_page()
    pdf.image(qr_code_path, x=60, y=60, w=90)
    pdf.set_y(160)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'ID: {id_str}', 0, 1, 'C')

# Save PDF to file
pdf_path = "encrypted_qrs.pdf"
pdf.output(pdf_path)

print(f"PDF saved to {pdf_path}")
