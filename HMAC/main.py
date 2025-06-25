"""
    Arquivo Principal
"""
from estacao import receber_dados_estacao, hash_senha, autenticar_mensagem, salvar_json
#from servidor import

senha = input("Digite sua senha: ")

temperatura = 23.5
umidade = 65
pressao = 1012

# Processamento
dados = receber_dados_estacao(temperatura, umidade, pressao)
chave = hash_senha(senha)
mensagem = autenticar_mensagem(dados, chave)

# Salvando a mensagem
salvar_json(mensagem)