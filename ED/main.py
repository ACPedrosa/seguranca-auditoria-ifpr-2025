# main.py
from EnvelopDigital import EnvelopDigital
from Destinatario import Destinatario
from seguranca import gerar_chaves_rsa

def main():
    # --- Gerar chaves RSA do destinatário ---
    chave_privada, chave_publica = gerar_chaves_rsa()
    #print("Chave pública e chave privada geradas.\n")

    # --- Criação do envelope digital ---
    print("----- Crie seu envelope digital -----\n")
    envelope = EnvelopDigital(chave_publica)

    # Executa a FSM até ENVIAR
    while envelope.estado_atual != envelope.estado_atual.ENVIAR:
        envelope.fsm()

    envelope.fsm() 
    print("Envelope digital salvo em 'envelope.json'.\n")

    # --- Menu ---
    while True:
        print("\nEscolha uma opção:")
        print("1 - Decifrar a mensagem")
        print("2 - Sair")
        opcao = input("Digite sua opção: ").strip()

        if opcao == "1":
            destinatario = Destinatario(chave_privada)
            mensagem_recebida = destinatario.abrir_envelope("ED/envelope.json")
            print("\nMensagem recebida:", mensagem_recebida)
        elif opcao == "2":
            print("Saindo do programa")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
