import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import padding

import secrets
from hashlib import sha256


"""
    Criptografia Simétrica - geração de AES e IV
"""
def criar_chave_aes():
    return secrets.token_bytes(32)

def create_iv():
    iv = secrets.token_bytes(16) #gerador de números pseudoaleatórios
    return iv

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

def decrypt_aes(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    """
    Descriptografa o texto cifrado usando AES no modo CBC.

    :param key: Chave de criptografia de 16, 24 ou 32 bytes.
    :param iv: Vetor de inicialização de 16 bytes.
    :param ciphertext: Texto cifrado a ser descriptografado.
    :return: Texto em claro.
    """
    # Criação do cifrador AES no modo CBC
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )

    # Criando o objeto de descriptografia
    decryptor = cipher.decryptor()

    # Descriptografando o texto cifrado
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remoção do preenchimento
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext


""" 
    Criptografia Assim[etrica - geração de rsa
"""

def gerar_chaves_rsa(tamanho=3072):
    """
    Gera par de chaves RSA (privada e pública).
    :param tamanho: tamanho da chave rsa

    :return: chaves privada e pública
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=tamanho,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()

def criptografar_rsa(mensagem: bytes, public_key):
    """
    Criptografa uma mensagem com chave pública RSA.
    
    :param mensagem: mensagem que será criptografada
    :param public_key: chave pública

    :return: mensagem criptografada com a chave pública
    """
    padding_config = asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )

    mensagem_cript = public_key.encrypt(mensagem, padding_config)

    return mensagem_cript

def descriptografar_rsa(ciphertext: bytes, private_key):
    """
    Descriptografa uma mensagem com chave privada RSA.
    
    :param ciphertext: menssagem cifrada
    :param private_key: chave privada do destiatário

    :return: ensagem descriptografada
    """
    padding_config = asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )

    mensagem_decript = private_key.decrypt(ciphertext, padding_config)

    return mensagem_decript


"""
    Ações do Usuário - mensagem
"""

def ler_mensagem():
    mensagem = input("Digite sua mensagem: ")
    return mensagem

def salvar_mensagem(mensagem_cifrada, chave_aes_cript, iv,  arquivo="ED/envelope.json"):
        envelope = {
                "mensagem_cifrada": mensagem_cifrada.hex(),
                "chave_aes_cifrada": chave_aes_cript.hex(),
                "iv": iv.hex()
                        }
        with open(arquivo, "w") as f:
            json.dump(envelope, f)