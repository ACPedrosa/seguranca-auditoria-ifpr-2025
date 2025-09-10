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

def criar_chave_privada():
  private_key = rsa.generate_private_key(
                                          public_exponent=65537,
                                          key_size=3072,
                                          backend=default_backend(),
                                        )
  return private_key

def ler_chave_privada_pem_to_str(private_key):
  # Exportar em PEM (texto legível)
  pem_private = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
  )

  pem_private = str(pem_private.decode()).replace("\n", "")
  return pem_private


def converter_chave_privada_str_to_pem(private_key):
  private_key = private_key.encode()
  pem_private = serialization.load_pem_private_key(
      private_key,
      password=None,
      backend=default_backend()
  )
  return pem_private

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