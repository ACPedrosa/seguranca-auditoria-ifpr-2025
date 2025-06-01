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

def header_validation(header):
    if header["ident"] != b'ED':
        print("Arquivo inválido: identificador incorreto.")
    if header["version"] != 0x01:
        print("Versão não suportada.")
    if header["algo"] != 0x01:
        print("Algoritmo não suportado.")
    if header["mode"] != 0x01:
        print("Modo de operação não suportado (esperado CBC).")
    return True

def create_key():
    senha = input("Digite a senha do arquivo: ").encode()
    chave = hashlib.sha256(senha).digest()  # 256 bits (32 bytes)
    return chave

