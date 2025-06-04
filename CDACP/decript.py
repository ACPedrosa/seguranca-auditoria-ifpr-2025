from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from hashlib import sha256
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
        print("Versão incorreta.")
    if header["algo"] != 0x01:
        print("Algoritmo incorreto.")
    if header["mode"] != 0x01:
        print("Modo de operação inválido")
    return True

def create_key():
    senha = input("Digite a senha do arquivo: ").encode()
    chave = hashlib.sha256(senha).digest()  
    return chave

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

def save_file(nome_arquivo: str, dados: bytes):
    novo_nome = nome_arquivo.replace(".enc", ".dec")
    with open(novo_nome, "wb") as f:
        f.write(dados)
    

# === Execução principal ===
arquivo = input("Digite o caminho do arquivo criptografado: ")

if not os.path.isfile(arquivo):
    print("Arquivo não encontrado.")
else:
    header = read_header(arquivo)
    try:
        header_validation(header)
    except ValueError as e:
        print("Erro de validação do cabeçalho:", e)
        exit()

    chave = create_key()

    with open(arquivo, "rb") as f:
        f.seek(48) 
        conteudo_cifrado = f.read()

    try:
        texto_decifrado = decrypt_aes(chave, header["iv"], conteudo_cifrado)
        save_file(arquivo, texto_decifrado)
    except Exception as e:
        print("Erro ao decifrar:", e)

