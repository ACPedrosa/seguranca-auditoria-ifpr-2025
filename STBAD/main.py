"""
    -- Arquivo Principal --
"""

from Usuario import *
from Transacao import Transacao
from datetime import datetime
import time
import json

def menu():
    print("=" * 55)
    print(f"{' '*18} Sistema  Bancário")
    print("=" * 55)
    print("1 - Cadastro de Usuario")
    print("2 - Realizar transação")
    print("3 - Consultar saldo")
    print("4 - Validar Assinatura")
    print("5 - Ver histórico de transações")
    print("0 - Sair")
    print("=" * 55)

def main():
    print("=" * 55)
    print(f"{' '*18} Bem-vindo ao Banco Silva")
    print("=" * 55)

    while True:
        menu()
        n_operacao = str(input("Escolha uma operação: "))

        match n_operacao:    
            case '1':
                    # Cadastro de Usuário
                    print(f"---- Cadastro ----\n")
                    nome = str(input("Digite nome de usuario: "))
                    usuario = cadrastrar_usuario(nome)
                    


            case '2':
                print(f"\n--- Realizando transação ---\n")
                nome_dest = str(input("Digite o nome do destinatário: "))
                valor = float(input("Digite o valor a ser transferido: R$ "))

                # Aqui futuramente: validação de senha
                transacao = usuario.criar_transacao(nome_dest, valor)

                if usuario.verificar_transacao(transacao):
                    transacao.log_transacao()
                    print("Transação concluída com sucesso!\n")
                else:
                    print("Transação não autorizada!\n")

                time.sleep(1.5)

            case '3':
                print(f"\nSeu saldo atual é: R$ {usuario._saldo:.2f}\n")
                time.sleep(1.5)

            case '5':
                try:
                    with open("./STBAD/log_transacoes.json", "r", encoding="utf-8") as f:
                        hTransacoes = json.load(f)

                    # Filtrar apenas as do usuário
                    historico_usuario = [
                        t for t in hTransacoes if t["remetente"] == usuario.getNome() or t["destinatario"] == usuario.getNome()
                    ]

                    if not historico_usuario:
                        print("Nenhuma transação encontrada.\n")
                        break

                    print(f"\nHistórico de transações de {usuario.getNome()}:\n")
                    for t in historico_usuario:
                        print(f"Data: {t['data_hora']}")
                        print(f"De: {t['remetente']}  ->  Para: {t['destinatario']}")
                        print(f"Valor: R$ {t['valor']:.2f}")
                        print(f"Status: {t['status']}")
                        print("-" * 40)
                    
                except FileNotFoundError:
                    print("Nenhuma transação encontrada.\n")
                except json.JSONDecodeError:
                    print("Erro ao ler o histórico (JSON inválido).\n")

                time.sleep(2)
                break

            case '0':
                print("\nObrigado por usar nosso sistema bancário! \n")
                break

            case _:
                print("\n Opção inválida! Tente novamente.\n")
                time.sleep(1)

if __name__ == "__main__":
    main()
