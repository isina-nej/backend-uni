#!/usr/bin/env python3
"""
Generate a new Django secret key for production
"""
import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key."""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Secret Key:")
    print(secret_key)
    print("\nAdd this to your .env.production file:")
    print(f"SECRET_KEY={secret_key}")
