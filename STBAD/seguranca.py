"""
    seguranca - arquivo destinado a implementação da parte de segurança do sistema e transação bancário
    @autor(a): Ana Caroline Pedrosa
    Date: 03/09/2025
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os

def criar_chave_privada():
  private_key = rsa.generate_private_key(
                                          public_exponent=65537,
                                          key_size=3072,
                                          backend=default_backend(),
                                        )
  return private_key

def save_private_key_file(private_key, nome):
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(), )
    
    private_path = f"./STBAD/rsa_keys/private_key_{nome}.pem"

    if os.path.exists(private_path):
        return

    os.makedirs(os.path.dirname(private_path), exist_ok=True)

    with open(private_path, 'xb') as private_file:
        private_file.write(private_bytes)

def ler_chave_privada_pem_to_str(private_key):
  # Exportar em PEM (texto legível)
  pem_private = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
  )

  pem_private = str(pem_private.decode()).replace("\n", "")
  return pem_private

def carregar_chave_publica_de_arquivo(nome):
    caminho_arquivo = f"./STBAD/rsa_keys/private_key_{nome}.pem"

    with open(caminho_arquivo, 'rb') as pem_file:
        pem_data = pem_file.read()
    private_key = serialization.load_pem_private_key(
        pem_data,
        password=None,
        backend=default_backend()
    )
    return private_key

def ler_chave_publica_pem_to_str(public_key):
  pem_str = public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
  ).decode('utf-8')

  pem_str = pem_str.replace("\n", "")
  return pem_str


def converter_chave_privada_str_to_pem(private_key):
  private_key = private_key.encode()
  pem_private = serialization.load_pem_private_key(
      private_key,
      password=None,
      backend=default_backend()
  )
  return pem_private


def converter_chave_public_str_to_pem(pem_str):
  public_key = serialization.load_pem_public_key(
    pem_str.encode('utf-8'),
    backend=default_backend()
  )

  return public_key
  

def criar_chave_publica(private_key):
  public_key = private_key.public_key()
  
  return public_key

def config_padding():
  padding_config = padding.PSS(
                              mgf=padding.MGF1(hashes.SHA256()),
                              salt_length=padding.PSS.MAX_LENGTH
                            )
  return padding_config

def assinar_dados(private_key, message, padding_config):
  signature = private_key.sign(
                              message,
                              padding_config,
                              hashes.SHA256()
                            )
  return signature

def verificar_assinatura(public_key, message: bytes, signature: bytes, padding_config) -> bool:
    try:
        public_key.verify(
            signature,
            message,
            padding_config,
            hashes.SHA256()
        )
        return True
    except Exception:
        return False