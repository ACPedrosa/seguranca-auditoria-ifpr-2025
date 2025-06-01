from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import hashlib
import os

def read_header(arquivo):
    with open(arquivo, "rb") as f:
        data = f.read(48)
    
    header = {
        "ident": data[0:2],
        "version": data[2],
        "algo": data[3],
        "mode": data[4],
        "iv": data[5:21],
        "fingerprint": data[21:37],  # não usado no momento
        "reserved": data[37:48]
    }
    return header


