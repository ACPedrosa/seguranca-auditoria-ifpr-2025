"""
    --- Estação Metereológica ---
    A estação deve enviar os dados assinados para o servidor
        - Aplicando HMAC
"""
import hashlib
import hmac
import json
import os
import secrets


def receber_dados_estacao(temperatura:float, umidade:float, pressao:float) -> dict:
    """
    Recebe os dados da estação e gera um dicionário 

    Parâmetros:
        temperatura(float): dado de temperatura
        umidade(float): dado de umidade
        pressao(float): dado de pressao atmosférica

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
        senha(str): senha receida do usuário
    Retorno:
        chave_secreta: hash da senha com o salt
    """
    # Gerar um salt aleatório de 16 bytes
    salt = secrets.token_bytes(16)

    iterations = 100

    chave_secreta = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt, iterations)

    return salt, chave_secreta

def autenticar_mensagem(dados: dict, chave_secreta: bytes) -> bytes:
    """
    Gera uma mensagem autenticada com HMAC-SHA256.

    Parâmetros:
        dados (dict): dados da estação meteorológica.
        chave (bytes): chave secreta usada para gerar o HMAC.

    Retorno:
        bytes: arquivo com os dados originais e o HMAC gerado.
    """

    dados_json = json.dumps(dados, sort_keys=True).encode()

    # Gera o HMAC com SHA-256
    hash_hmac = hmac.new(chave_secreta, dados_json, hashlib.sha256).hexdigest()

    # Retorna os dados 
    mensagem = {
        "dados": dados,
        "hmac": hash_hmac
    }

    return mensagem

def salvar_json(mensagem: dict):
    """
    Salva a mensagem em um arquivo jason na pasta 'dados'.

    Parâmetros:
        mensagem (dict): mensagem autenticada com os dados e o HMAC.
    """
    os.makedirs("dados", exist_ok=True)
    with open("dados/dados_estacao.json", "w", encoding="utf-8") as f:
        json.dump(mensagem, f, ensure_ascii=False, indent=4)

