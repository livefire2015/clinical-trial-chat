"""
Data encryption utilities for sensitive clinical trial data
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


def get_encryption_key() -> bytes:
    """
    Get or generate encryption key from environment

    Returns:
        bytes: Fernet encryption key
    """
    key_string = os.getenv("ENCRYPTION_KEY")

    if not key_string:
        # Generate a new key if none exists (development only)
        return Fernet.generate_key()

    # Derive key from string using PBKDF2
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"clinical_trial_salt",  # In production, use a secure random salt
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(key_string.encode()))
    return key


def encrypt_data(data: str) -> str:
    """
    Encrypt sensitive data

    Args:
        data: Plain text data to encrypt

    Returns:
        str: Encrypted data as base64 string
    """
    key = get_encryption_key()
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_data(encrypted_data: str) -> str:
    """
    Decrypt sensitive data

    Args:
        encrypted_data: Base64 encoded encrypted data

    Returns:
        str: Decrypted plain text
    """
    key = get_encryption_key()
    f = Fernet(key)
    decoded = base64.urlsafe_b64decode(encrypted_data.encode())
    decrypted = f.decrypt(decoded)
    return decrypted.decode()


def encrypt_dict_values(data: dict, keys_to_encrypt: list[str]) -> dict:
    """
    Encrypt specific values in a dictionary

    Args:
        data: Dictionary with data
        keys_to_encrypt: List of keys whose values should be encrypted

    Returns:
        dict: Dictionary with encrypted values
    """
    result = data.copy()
    for key in keys_to_encrypt:
        if key in result and result[key]:
            result[key] = encrypt_data(str(result[key]))
    return result


def decrypt_dict_values(data: dict, keys_to_decrypt: list[str]) -> dict:
    """
    Decrypt specific values in a dictionary

    Args:
        data: Dictionary with encrypted data
        keys_to_decrypt: List of keys whose values should be decrypted

    Returns:
        dict: Dictionary with decrypted values
    """
    result = data.copy()
    for key in keys_to_decrypt:
        if key in result and result[key]:
            try:
                result[key] = decrypt_data(result[key])
            except Exception:
                # If decryption fails, leave the value as is
                pass
    return result
