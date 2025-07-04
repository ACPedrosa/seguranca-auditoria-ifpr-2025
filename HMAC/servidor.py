from hmac import compare_digest
import hashlib
import hmac
import json



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
    
def verificar_mensagem(mensagem: dict, senha: str, salt:bytes) -> bool:
    """
    Verifica se os dados do arquivo json foram alterados

    Parametros:
        mensagem(dict): dicionário com os dados da estação
        senha(str): senha para autenticação de usuário
        salt(bytes): tempero utilizado no hahs da senha
    Retorno:
        boolean: true ou false da verificação
    """
    dados = mensagem['dados']
    hmac_json = mensagem['hmac']

    dados_json = json.dumps(dados, sort_keys=True).encode()

    chave_secreta = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt, 100)

    # Gera o HMAC com SHA-256
    hash_hmac = hmac.new(chave_secreta, dados_json, hashlib.sha256).hexdigest()

    # Verificar se o hash gerado corresponde ao hash armazenado
    return compare_digest( hmac_json,hash_hmac)


    


