"""
    --- Estação Metereológica ---
    A estação deve enviar os dados assinados para o servidor
        - Aplicando HMAC
"""
import hashlib
import hmac
import json
import secrets



def receber_dados_estação(temperatura:float, umidade:float, pressao:float) -> dict:
    """
    Recebe os dados da estação e gera um dicionário 

    Parâmetros:
        temperatura: dado de temperatura
        umidade: dado de umidade
        pressao: dado de pressao atmosférica

    Retorno:
        dict: dicionário com os dados da estação
    """
    dict_dados = {
        "temperatura": temperatura,
        "umidade": umidade,
        "pressao": pressao,
    }
    
    return dict_dados

def hash_senha(senha):
    """
    Gera o salt e o hash da senha com o salt

    Parâmetros:
        senha: senha receida do usuário
    Retorno:
        hashed_senha: hash da senha com o salt
    """
    # Gerar um salt aleatório de 16 bytes
    salt = secrets.token_bytes(16)

    # Criar uma instância do hash sha256
    hasher = hashlib.new('sha256')

    hasher.update(salt + senha.encode())

    hashed_senha = hasher.digest()

    return hashed_senha

def autenticar_mensagem(dados: dict, chave_secreta: bytes) -> bytes:
    """
    Gera uma mensagem autenticada com HMAC-SHA256.

    Parâmetros:
        dados (dict): dados da estação meteorológica.
        chave (bytes): chave secreta usada para gerar o HMAC.

    Retorno:
        bytes: arquivo com os dados originais e o HMAC gerado.
    """

    mensagem = b'ana'
    return mensagem

