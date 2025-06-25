"""
    -- Arquivo Principal --
"""
from estacao import receber_dados_estacao, hash_senha, autenticar_mensagem, salvar_json
from servidor import ler_json, verificar_mensagem

#---- Ações da estação ----
senha01 = input("Digite sua senha para enviar os dados ao servidor: ")

temperatura = 17.0
umidade = 56
pressao = 1000

dados = receber_dados_estacao(temperatura, umidade, pressao)
salt, chave = hash_senha(senha01)
mensagem = autenticar_mensagem(dados, chave)

salvar_json(mensagem)

# ---- Ações do servidor ----
senha02 = input("Para verificar os dados da estação, digite sua senha: ")

caminho = "dados/dados_estacao.json"
mensagem_server = ler_json(caminho)

if(verificar_mensagem(mensagem_server, senha02, salt)):
    print("Sua mensagem não foi alterada")
else:
    print("Sua mensagem foi alterada")
