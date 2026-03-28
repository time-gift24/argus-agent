"""AES-256-GCM encryption utilities.

All provider configs are stored encrypted. Each encryption uses a random IV.
Output format: base64(iv || ciphertext || tag)
"""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


@dataclass(frozen=True)
class EncryptedData:
    """Result of an encryption operation."""

    ciphertext_b64: str


@dataclass(frozen=True)
class VersionedEncrypted:
    """Encrypted data with a version prefix for key rotation."""

    version: str
    ciphertext_b64: str


def encrypt(plaintext: str, key: bytes) -> str:
    """
    Encrypt plaintext with AES-256-GCM.

    Args:
        plaintext: UTF-8 string to encrypt.
        key: 32-byte AES key.

    Returns:
        base64(iv || ciphertext || tag) with no version prefix.
    """
    aesgcm = AESGCM(key)
    iv = os.urandom(12)  # 96-bit nonce for GCM
    ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8"), None)
    # ciphertext = ciphertext || tag (tag is appended by AESGCM)
    return base64.b64encode(iv + ciphertext).decode("ascii")


def decrypt(encrypted_b64: str, key: bytes) -> str:
    """
    Decrypt AES-256-GCM encrypted data.

    Supports versioned format: "v1:..." falls back to unprefixed.

    Args:
        encrypted_b64: base64 string, optionally prefixed with "vN:".
        key: 32-byte AES key.

    Returns:
        Decrypted UTF-8 string.

    Raises:
        ValueError: If decryption fails (tampered or wrong key).
    """
    versioned = _parse_versioned(encrypted_b64)
    return _decrypt_inner(versioned.ciphertext_b64, key)


def _parse_versioned(value: str) -> VersionedEncrypted:
    """Parse versioned encrypted value."""
    if value.startswith("v1:"):
        return VersionedEncrypted(version="v1", ciphertext_b64=value[3:])
    return VersionedEncrypted(version="", ciphertext_b64=value)


def _decrypt_inner(ciphertext_b64: str, key: bytes) -> str:
    """Decrypt without version parsing."""
    try:
        data = base64.b64decode(ciphertext_b64)
    except Exception as e:
        raise ValueError(f"Invalid base64: {e}") from e

    if len(data) < 12 + 16:
        raise ValueError("Encrypted data too short (need IV + tag)")

    iv = data[:12]
    ciphertext_with_tag = data[12:]
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(iv, ciphertext_with_tag, None)
    except Exception as e:
        raise ValueError(f"Decryption failed (tampered or wrong key): {e}") from e

    return plaintext.decode("utf-8")
