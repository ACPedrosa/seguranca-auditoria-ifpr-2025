import hashlib
import hmac
import json
import os
import secrets


def ler_json(caminho: str) -> dict:
    """
    Lê os dados do json e retorna um dicionário com esses dados

    Parâmetros:
        caminho(str): caminho do arquivo que será lido

    Retorno:
        dict: dicionário com os dados do json
    """
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
    
def verificar_mensagem(mensagem: dict, chave_secreta: bytes) -> bool:
    dados = mensagem['dados']
    hmac = mensagem['hmac']

    dados_json = json.dumps(dados, sort_keys=True).encode()

    # Gera o HMAC com SHA-256
    hash_hmac = hmac.new(chave_secreta, dados_json, hashlib.sha256).hexdigest()



