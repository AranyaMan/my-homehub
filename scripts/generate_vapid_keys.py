#!/usr/bin/env python3
"""
VAPID key generation utility for Web Push notifications.
Run this script to generate VAPID keys for push notification configuration.
"""
import base64
import sys
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


def generate_vapid_keys():
    """Generate VAPID key pair (P-256 elliptic curve)."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    
    # Private key in DER format (PKCS#8) then base64url encoded
    private_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_b64url = base64.urlsafe_b64encode(private_der).decode('utf-8').rstrip('=')
    
    # Public key in uncompressed point format (0x04 + X + Y) then base64url encoded
    public_numbers = public_key.public_numbers()
    x = public_numbers.x.to_bytes(32, byteorder='big')
    y = public_numbers.y.to_bytes(32, byteorder='big')
    public_uncompressed = b'\x04' + x + y
    public_b64url = base64.urlsafe_b64encode(public_uncompressed).decode('utf-8').rstrip('=')
    
    return {
        'private_key': private_b64url,
        'public_key': public_b64url
    }


def main():
    keys = generate_vapid_keys()
    print("VAPID Keys Generated:")
    print(f"Public Key:  {keys['public_key']}")
    print(f"Private Key: {keys['private_key']}")
    print()
    print("Add these to your config.yml:")
    print("push_notifications:")
    print(f"  vapid_public_key:  \"{keys['public_key']}\"")
    print(f"  vapid_private_key: \"{keys['private_key']}\"")
    print('  vapid_subject: "mailto:admin@yourdomain.com"')


if __name__ == '__main__':
    main()