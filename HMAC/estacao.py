"""
    --- Estação Metereológica ---
    A estação deve enviar os dados assinados para o servidor
        - Aplicando HMAC
"""

# Dados da estação

dados = {
    "temperatura": 25.3,
    "umidade": 60.2,
    "pressao": 1013.2,
}

def autenticar_mensagem(dados: dict, chave_secrete: bytes) -> bytes:
    """
    Gera uma mensagem autenticada com HMAC-SHA256.

    Parâmetros:
        dados (dict): dados da estação meteorológica.
        chave (bytes): chave secreta usada para gerar o HMAC.

    Retorno:
        bytes: arquivo com os dados originais e o HMAC gerado.
    """
    mensagem = b'ana'
    return mensagem;