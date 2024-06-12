import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Encryption key (must be 16, 24, or 32 bytes long)
encryption_key = b'ada7327441e9876aaa5f19d8262c9482'[:16]  # Ensure it's 16 bytes for AES-128

# Fixed IV for example purposes (should be 16 bytes)
iv = b'1234567890123456'

def decrypt(enc_data, key):
    enc_data = base64.b64decode(enc_data)
    iv = enc_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(enc_data[AES.block_size:]), AES.block_size)
    return decrypted_data.decode('utf-8')

# Encrypted data from the scanned QR code
scanned_qr_data = "MTIzNDU2Nzg5MDEyMzQ1NkDNVdl1cy5NqROwR2V+70kb0MxxnIsMHHbu0mPhVMNP29GpH3xAAWJ3HSAhFrVwFA=="

# Decrypt the data
decrypted_data = decrypt(scanned_qr_data, encryption_key)
print("Decrypted data:", decrypted_data)
