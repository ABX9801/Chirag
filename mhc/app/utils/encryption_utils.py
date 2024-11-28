from config import CHAT_ENCRYPTION_KEY
from cryptography.fernet import Fernet

ENCODED_ENCRYPTION_KEY = CHAT_ENCRYPTION_KEY.encode('utf-8')

def encrypt_text(message):
    cipher_cuite = Fernet(ENCODED_ENCRYPTION_KEY)
    encrypted_message = cipher_cuite.encrypt(message.encode('utf-8'))
    return encrypted_message.decode('utf-8')

def decrypt_text(encrypted_message):
    encrypted_message = encrypted_message.encode('utf-8')
    cipher_cuite = Fernet(ENCODED_ENCRYPTION_KEY)
    decrypted_message = cipher_cuite.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message
