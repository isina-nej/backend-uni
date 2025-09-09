#!/usr/bin/env python3
"""
Generate Django SECRET_KEY
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for i in range(length))

if __name__ == "__main__":
    print("🔐 Generated SECRET_KEYs:")
    print("=" * 60)
    for i in range(3):
        key = generate_secret_key()
        print(f"Option {i+1}: {key}")
    print("=" * 60)
    print("Pick one and use it in your .env file!")
