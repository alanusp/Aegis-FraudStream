# SPDX-License-Identifier: Apache-2.0
"""Optional KMS adapters. Use envelope encryption if configured."""
import os, base64, json, typing as t
from typing import Optional

class NullKMS:
    def encrypt(self, plaintext: bytes) -> bytes: return plaintext
    def decrypt(self, ciphertext: bytes) -> bytes: return ciphertext

def get_kms():
    provider = (os.getenv("AEGIS_KMS_PROVIDER") or "").lower()
    if provider == "aws":
        try:
            import boto3  # type: ignore
            key_id = os.getenv("AEGIS_KMS_KEY_ID")
            if not key_id: return NullKMS()
            class _AWS:
                def __init__(self, kid): self.client=boto3.client("kms"); self.key_id=kid
                def encrypt(self, plaintext: bytes) -> bytes:
                    r=self.client.encrypt(KeyId=self.key_id, Plaintext=plaintext); return r["CiphertextBlob"]
                def decrypt(self, ciphertext: bytes) -> bytes:
                    r=self.client.decrypt(CiphertextBlob=ciphertext); return r["Plaintext"]
            return _AWS(key_id)
        except Exception:
            return NullKMS()
    return NullKMS()
