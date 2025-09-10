"""
 Atividade: envelope digital
    Passos:
      - Gerar uma chave(AES)
      - Cifrar os dados com a chave gerada
      - Cifrar a chave gerada (AES) com a Chave pública do destinatário
      - Enviar os dados e chave pública (gerar com RSA)
"""

from enum import Enum
from seguranca import ler_mensagem, criar_chave_aes, create_iv, encrypt_aes, criptografar_rsa, salvar_mensagem

class EstadosEnvelope(Enum):
    INICIAL = 1
    CRIAR_AES = 2
    CRIPT_MENSAGEM = 3
    CRIPT_CHAVE = 4
    ENVIAR = 5

class EnvelopDigital:
    def __init__(self, chave_publica_destinatario):
        #estadis
        self.estado_atual = EstadosEnvelope.INICIAL

        #variáveis
        self.mensagem = None
        self.chave_aes_bytes = None
        self.iv = None
        self.mensagem_cifrada = None
        self.chave_aes_cript = None

        # Chave pública do destinatário
        self.chave_publica_dest = chave_publica_destinatario

    def fsm(self):
        match self.estado_atual:

            case EstadosEnvelope.INICIAL:
                self.mensagem = ler_mensagem()
                
                self.estado_atual = EstadosEnvelope.CRIAR_AES

            case EstadosEnvelope.CRIAR_AES:
                self.chave_aes_bytes = criar_chave_aes()
                self.iv = create_iv()

                self.estado_atual = EstadosEnvelope.CRIPT_MENSAGEM

            case EstadosEnvelope.CRIPT_MENSAGEM:
                self.mensagem_cifrada = encrypt_aes(self.chave_aes_bytes, self.iv, self.mensagem.encode())

                self.estado_atual = EstadosEnvelope.CRIPT_CHAVE
            
            case EstadosEnvelope.CRIPT_CHAVE:
                self.chave_aes_cript = criptografar_rsa(self.chave_aes_bytes, self.chave_publica_dest)

                self.estado_atual = EstadosEnvelope.ENVIAR

            case EstadosEnvelope.ENVIAR:
                #salvar em arqivo a chave aes cropt e a mensagem
                salvar_mensagem(self.mensagem_cifrada, self.chave_aes_cript, self.iv)
