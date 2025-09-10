import json

from seguranca import descriptografar_rsa, decrypt_aes

class Destinatario:
    def __init__(self, chave_privada):
        self.chave_privada = chave_privada
        self.chave_aes = None
        self.iv = None
        self.mensagem = None

    def abrir_envelope(self, arquivo="ED/envelope.json"):
        with open(arquivo, "r") as f:
            envelope = json.load(f)

        # Converter de hex para bytes
        mensagem_cifrada = bytes.fromhex(envelope["mensagem_cifrada"])
        chave_aes_cript = bytes.fromhex(envelope["chave_aes_cifrada"])
        self.iv = bytes.fromhex(envelope["iv"])

        self.chave_aes = descriptografar_rsa(chave_aes_cript, self.chave_privada)

        self.mensagem = decrypt_aes(self.chave_aes, self.iv, mensagem_cifrada)
        return self.mensagem