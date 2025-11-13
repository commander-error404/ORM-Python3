from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, base64

def aes_gcm_encrypt(key: bytes, plaintext: str, aad: bytes = None):
    """
    Encrypts a UTF-8 string with AES-256-GCM.
    Returns Base64 ciphertext and nonce.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # ----- 96-bit nonce recommended for GCM
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), aad)
    # ----- AESGCM.encrypt returns ciphertext || tag
    return base64.b64encode(nonce + ciphertext).decode()

def aes_gcm_decrypt(key: bytes, b64_ciphertext: str, aad: bytes = None):
    """
    Decrypts Base64 ciphertext created by aes_gcm_encrypt().
    """
    data = base64.b64decode(b64_ciphertext)
    nonce, ciphertext = data[:12], data[12:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, aad)
    return plaintext.decode()

# ======== Example usage ========

# ----- 32 bytes = AES-256 key
# key = os.urandom(32)

# text = "Hello World!"
# aad = b"optional-associated-data"

# encrypted = aes_gcm_encrypt(key, text, aad)
# print("Encrypted (Base64):", encrypted)

# decrypted = aes_gcm_decrypt(key, encrypted, aad)
# print("Decrypted:", decrypted)
