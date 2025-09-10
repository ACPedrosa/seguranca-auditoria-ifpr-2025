"""
    -- Arquivo Principal --
"""

from Usuario import Usuario, cadrastrar_usuario
from Transacao import Transacao
from datetime import datetime
import time
import json

def menu():
    print("=" * 55)
    print(f"{' '*18} Sistema  Bancário")
    print("=" * 55)
    print("1 - Realizar transação")
    print("2 - Consultar saldo")
    print("3 - Ver histórico de transações")
    print("0 - Sair")
    print("=" * 55)

def main():
    print("=" * 55)
    print(f"{' '*18} Bem-vindo ao Banco Silva")
    print("=" * 55)

    # Cadastro de Usuário
    print(f"---- Cadastro ----\n")
    nome = str(input("Digite seu nome: "))
    usuario = cadrastrar_usuario(nome)

    while True:
        menu()
        n_operacao = str(input("Escolha uma operação: "))

        match n_operacao:
            case '1':
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

            case '2':
                print(f"\nSeu saldo atual é: R$ {usuario._saldo:.2f}\n")
                time.sleep(1.5)

            case '3':
                try:
                    with open("./log_transacoes.json", "r", encoding="utf-8") as f:
                        hTransacoes = json.load(f)

                    # Filtrar apenas as do usuário
                    historico_usuario = [
                        t for t in hTransacoes if t["remetente"] == usuario.getNome() or t["destinatario"] == usuario.getNome()
                    ]

                    if not historico_usuario:
                        print("Nenhuma transação encontrada.\n")
                        return

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

            case '0':
                print("\nObrigado por usar nosso sistema bancário! \n")
                break

            case _:
                print("\n Opção inválida! Tente novamente.\n")
                time.sleep(1)

if __name__ == "__main__":
    main()
