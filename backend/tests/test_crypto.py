"""Unit tests: AES-256-GCM crypto."""

import base64

import pytest

from app.core.crypto import decrypt, encrypt


class TestEncryptDecryptRoundtrip:
    def test_encrypt_decrypt_roundtrip(self):
        plaintext = '{"api_key": "sk-abc123", "base_url": "https://api.openai.com"}'
        key = b"0" * 32

        encrypted = encrypt(plaintext, key)
        assert encrypted != plaintext
        assert ":" not in encrypted or encrypted.startswith("v1:")  # base64 has no colons

        decrypted = decrypt(encrypted, key)
        assert decrypted == plaintext

    def test_different_plaintexts_produce_different_ciphertexts(self):
        key = b"0" * 32
        enc1 = encrypt("hello", key)
        enc2 = encrypt("world", key)
        assert enc1 != enc2

    def test_empty_plaintext(self):
        key = b"0" * 32
        encrypted = encrypt("", key)
        decrypted = decrypt(encrypted, key)
        assert decrypted == ""


class TestDecryptDetectsTampering:
    def test_tampered_ciphertext_raises(self):
        key = b"0" * 32
        encrypted = encrypt("secret data", key)

        # Flip a bit in the ciphertext
        decoded_bytes = base64.b64decode(encrypted)
        tampered = bytes([decoded_bytes[0] ^ 0xFF]) + decoded_bytes[1:]
        tampered_b64 = base64.b64encode(tampered).decode()

        with pytest.raises(ValueError, match="Decryption failed"):
            decrypt(tampered_b64, key)

    def test_wrong_key_raises(self):
        key1 = b"A" * 32
        key2 = b"B" * 32

        encrypted = encrypt("secret", key1)
        with pytest.raises(ValueError, match="Decryption failed"):
            decrypt(encrypted, key2)

    def test_malformed_base64_raises(self):
        key = b"0" * 32
        with pytest.raises(ValueError, match="Invalid base64"):
            decrypt("not-valid-base64!!!", key)

    def test_truncated_data_raises(self):
        key = b"0" * 32
        short = base64.b64encode(b"too-short").decode()
        with pytest.raises(ValueError, match="too short"):
            decrypt(short, key)
