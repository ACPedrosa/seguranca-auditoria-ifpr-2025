"""
    -- Arquivo Principal --
"""
from estacao import receber_dados_estacao, hash_senha, autenticar_mensagem, salvar_json
from servidor import ler_json

#---- Ações da estação ----
senha = input("Digite sua senha: ")

temperatura = 17.0
umidade = 56
pressao = 1000

# Processamento
dados = receber_dados_estacao(temperatura, umidade, pressao)
salt, chave = hash_senha(senha)
mensagem = autenticar_mensagem(dados, chave)

# Salvando a mensagem
salvar_json(mensagem)

# ---- Ações do servidor ----

caminho = "dados/dados_estacao.json"
mensagem_server = ler_json(caminho)



#validar o arquivo