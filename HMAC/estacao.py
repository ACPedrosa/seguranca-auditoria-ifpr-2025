"""
    --- Estação Metereológica ---
    A estação deve enviar os dados assinados para o servidor
        - Aplicando HMAC
"""

def receber_dados_estação(temperatura, umidade, pressao) -> dict:
    dict_dados = {
        "temperatura": temperatura,
        "umidade": umidade,
        "pressao": pressao,
    }
    
    return dict_dados


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
    return mensagem