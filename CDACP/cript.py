
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
import secrets
import hashlib
import os

def read_file(arquivo):
    with open(arquivo, "rb") as f:
        arqBin = f.read()
    return arqBin

def create_key():
    senha = input("Digite a senha do arquivo: ").encode()
    chave = hashlib.sha256(senha).digest()
    return chave
    
def create_iv():
    iv = secrets.token_bytes(16)
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

def save_file(header, enc, arquivo):
    completo = header + enc
  # Salvar o arquivo
    with open(arquivo +'.enc', "wb") as f:
        f.write(completo)


# === Main ===
arquivo = input("Digite o caminho do seu arquivo: ")
if not os.path.isfile(arquivo):
    print("Arquivo não encontrado.")
else:
    arqBin = read_file(arquivo)
    chave = create_key()
    iv = create_iv()
    enc = encrypt_aes(chave, iv, arqBin)
    header = create_header(iv)
    save_file(header, enc, arquivo)
    