from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def gerar_chaves(tamanho=3072):
    """Gera par de chaves RSA (privada e pública)."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=tamanho,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def salvar_chave_privada(private_key, caminho='private_key.pem'):
    """Salva chave privada em formato PEM (PKCS8, sem senha)."""
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(caminho, 'wb') as f:
        f.write(private_bytes)


def salvar_chave_publica(public_key, caminho='public_key.pem'):
    """Salva chave pública em formato PEM."""
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(caminho, 'wb') as f:
        f.write(public_bytes)


def carregar_chave_privada(caminho='private_key.pem'):
    """Carrega chave privada de arquivo PEM."""
    with open(caminho, 'rb') as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )


def carregar_chave_publica(caminho='public_key.pem'):
    """Carrega chave pública de arquivo PEM."""
    with open(caminho, 'rb') as f:
        return serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )


def criptografar(mensagem: bytes, public_key):
    """Criptografa uma mensagem com chave pública RSA."""
    padding_config = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
    return public_key.encrypt(mensagem, padding_config)


def descriptografar(ciphertext: bytes, private_key):
    """Descriptografa uma mensagem com chave privada RSA."""
    padding_config = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
    return private_key.decrypt(ciphertext, padding_config)

