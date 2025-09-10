"""
 Atividade: envelope digital
    Passos:
      - Gerar uma chave(AES)
      - Cifrar os dados com a chave gerada
      - Cifrar a chave gerada (AES) com a Chave pública do destinatário
      - Enviar os dados e chave pública (gerar com RSA)
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

import secrets
from hashlib import sha256
import os

def read_file(arquivo):
    with open(arquivo, "rb") as f:
        arqBin = f.read()
    return arqBin

#SHA256 vai gerar uma hash que sempre vai medir 256 bits, ou seja, 32 bytes.
def create_key():
    senha = input("Digite a senha do arquivo: ")
    hash_senha = sha256(senha.encode()).digest()
    return hash_senha

def cript_key(aesKey: bytes, public_key: bytes) -> bytes:
    chave  = 'vv'
    return chave
 
#Fazer um cabeçaçalho: primeira pos: mensagem; seg: chave dentro de um arquivo.txt
def enviar_dados(mensagem_cifrada: bytes, chave_cifrada: bytes):
    with open('envelope.bin', 'wb') as f:
        # Grava o tamanho da chave cifrada para poder separar depois
        f.write(len(chave_cifrada).to_bytes(4, 'big'))
        f.write(chave_cifrada)
        f.write(mensagem_cifrada)

def create_iv():
    iv = secrets.token_bytes(16)#gerador de números pseudoaleatórios
    return iv

def create_header(iv):
    # Motar o cabeçalho e concatenar
    header = bytearray()
    header += b'ED'
    header += bytes([0x01])  # versao
    header += bytes([0x01])  # algoritmo
    header += bytes([0x01])  # modo CBC
    header += iv
    header += bytes(11)

    return header


def encrypt_aes(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    """
    Criptografa o texto usando AES no modo CBC.

    :param key: Chave de criptografia de 16, 24 ou 32 bytes.
    :param iv: Vetor de inicialização de 16 bytes.
    :param plaintext: Texto em claro a ser criptografado.
    :return: Texto cifrado.
    """
    # Criação do cifrador AES no modo CBC
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )

    # Criando o objeto de criptografia
    encryptor = cipher.encryptor()

    # Preenchimento do texto em claro para ajustar ao tamanho do bloco
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    # Criptografando o texto em claro
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return ciphertext

def save_file(header, enc):
    completo = header + enc
  # Salvar o arquivo
    with open('concat.enc', "wb") as f:
        f.write(completo)

    
