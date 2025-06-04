from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from hashlib import sha256
import os


#SHA256 vai gerar uma hash que sempre vai medir 256 bits, ou seja, 32 bytes.
def create_key():
    senha = input("Digite a senha do arquivo: ")
    hash_senha = sha256(senha.encode()).digest()
    return hash_senha

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

def defHeaderMeta(iv, fingerprint):
    IDENT       = b'CF'                 # 2 bytes
    VERSION     = bytes([0x01])         # 1 byte
    ALGO        = bytes([0x01])         # 1 byte (AES)
    MODE        = bytes([0x01])         # 1 byte (CBC)
    IV          = iv     # 16 bytes: 0x00..0x0F
    FINGERPRINT = fingerprint     # 16 bytes: 0x10..0x1F
    RESERVED    = bytes(11)             # 11 bytes de 0x00

    # Monta o header (48 bytes)
    header = bytearray()
    header += IDENT
    header += VERSION
    header += ALGO
    header += MODE
    header += IV
    header += FINGERPRINT
    header += RESERVED

    if len(header) != 48:
            raise ValueError(f"Erro ao montar cabeçalho: tamanho incorreto. Esperado 48, obtido {len(header)}")

    return bytes(header) # Retorna como bytes imutáveis

def createMeta(nameFile, key):
    input_filepath = f'./arquivos/{nameFile}'
    output_filename = f'{nameFile}.meta'
    output_filepath = f'./meta/{output_filename}'

    try:
        os.makedirs('./meta', exist_ok=True)

        with open(input_filepath, 'rb') as f:
            originBinFile = f.read()

        iv = os.urandom(16) 
        enc = encrypt_aes(key, iv, originBinFile)
        fingerprint = enc[len(enc)-16:len(enc)]
        
        with open(output_filepath, 'wb') as f:
            header = defHeaderMeta(iv, fingerprint)
            f.write(header)

        print(f"\n✅ Criado o meta do '{nameFile}' com sucesso para '{output_filepath}'.")

    except FileNotFoundError:
        print(f"\n❌ Erro: O arquivo de entrada '{input_filepath}' não foi encontrado.")
    except ValueError as e:
        print(f"\n❌ Erro durante a meta: {e}")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado durante o meta de '{nameFile}': {e}")

def compararMeta(nameFile, key):
    input_filepath_meta = f'./meta/{nameFile}'
    input_filepath = f'./arquivos/{nameFile[:len(nameFile)-5]}'
    try:
        os.makedirs('./meta', exist_ok=True)

        with open(input_filepath_meta, 'rb') as f:
            data = f.read(48)

        if len(data) < 48:
            raise ValueError("Arquivo meta é muito pequeno para conter o cabeçalho completo.")

        ident      = data[0:2]        # 2 bytes
        version    = data[2]          # 1 byte
        algo       = data[3]          # 1 byte
        mode       = data[4]          # 1 byte
        iv         = data[5:21]       # 16 bytes
        fingerprint= data[21:37]      # 16 bytes
        reserved   = data[37:48]      # 11 bytes

        if ident.decode() != 'CF':
            raise ValueError(f"Identificador inválido no cabeçalho")
        if version != 1:
            raise ValueError(f"Versão inválida no cabeçalho")
        if algo != 1:
            raise ValueError(f"Algoritmo inválido no cabeçalho")
        if mode != 1:
            raise ValueError(f"Modo inválido no cabeçalho")

        if len(iv) != 16:
                raise ValueError(f"Tamanho do IV incorreto no cabeçalho: Esperado 16, obtido {len(iv)}")
        if len(fingerprint) != 16:
                raise ValueError(f"Tamanho do FINGERPRINT incorreto no cabeçalho: Esperado 16, obtido {len(fingerprint)}")

        with open(input_filepath, 'rb') as f:
            originBinFile = f.read()

        enc = encrypt_aes(key, iv, originBinFile)
        fingerprint_enc = enc[len(enc)-16:]

        print(f"\n✅ Arquivo {input_filepath} não sofreu alterações." if fingerprint == fingerprint_enc else f"\n❌ Arquivo {input_filepath} foi modificado")
        

    except FileNotFoundError:
        print(f"\n❌ Erro: O arquivo meta '{input_filepath_meta}' não foi encontrado. Certifique-se de que o arquivo .meta está em './meta/'.")
    except ValueError as e:
        print(f"\n❌ Erro de validação ou estrutura do arquivo meta: {e}")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado durante a comparação do meta: {e}")


os.makedirs('./meta', exist_ok=True)


nameFile_input = input("Informe o nome do arquivo.\nPara gerar o meta: 'nome_original.txt' (deve estar em './arquivos/')\nPara comparar o meta e o original: 'nome_original.meta' (deve estar em './meta/')\nNome do arquivo: ")

key = create_key()
#key = b'\xe1\x18\x89\xae\x98\xf7\x94\xf4+\x9bL\x89\xe0\x08W\xf8'

op = -1

while op not in [0, 1]:
    try:
        op = int(input("Qual operação ? 0 (Gerar Meta)\t1 (Comparar Meta)\nEscolha: "))
        if op not in [0, 1, 2]:
            print("❌ Opção inválida. Por favor, digite 0 para Gerar Meta ou 1 para Comparar Meta.")
    except ValueError:
        print("❌ Entrada inválida. Por favor, digite um número (0 ou 1).")

print("\n--- Iniciando Operação ---")

if op == 0:
    createMeta(nameFile_input, key)
elif op == 1:
    compararMeta(nameFile_input, key)
    
print("--- Operação Concluída ---\n")

