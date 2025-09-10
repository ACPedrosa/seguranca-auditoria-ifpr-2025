"""
    -- Arquivo Principal --
"""

from Usuario import Usuario, cadrastrar_usuario
from Transacao import Transacao

from datetime import datetime

#Cadastro de Usuários
print(f"---- Cadastro ----\n")
nome = str(input("Digite seu nome: "))
usuario = cadrastrar_usuario(nome)

print(f"---- Operações ----\n")
print("1 - Realizar transação\n2 - Consultar saldo\n3- Verificar histórico de transações\n")
print("Para sair do sistema digite 0")

n_operacao = str(input())

match n_operacao:
    case '1':
        print(f"--- Realizando transação ---\n")
        nome_dest = str(input("Digite o nome do destinatário: "))
        valor = float(input(f"Digite o valor a ser transferido: "))

        #fazer a validação de senha - fazer um banco fake com os hash de senha

        transacao = usuario.criar_transacao(nome_dest, valor)

        usuario.verificar_transacao(transacao)

        transacao.log_transacao()
    case '2':
        print(f"Seu saldo atual é: {usuario._saldo}")
    case '3':
        print(f"Histórico de transações")
        #abrir docs e printar na tela



