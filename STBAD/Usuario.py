"""
    Usuário - classe destinada aos atributos e funções do usuário do sistema
    @autor(a): Ana Caroline Pedrosa
    Date: 03/09/2025
"""
from Transacao import Transacao 
from seguranca import criar_chave_publica, criar_chave_privada, config_padding, assinar_dados

from datetime import datetime

class Usuario:
    def __init__(self, nome: str, saldo: float, chave_publica):
        self._nome = nome
        self._saldo = saldo
        self._chave_publica = chave_publica

     # Getter e Setter para nome
    def setNome(self, nome: str):
        self._nome = nome
    
    def getNome(self) -> str:
        return self._nome

     # Getter e Setter saldo
    def setSaldo(self, saldo: float):
        self._saldo = saldo

    def getSaldo(self)-> float:
        return self._saldo

    # Getter e Setter chave_publica
    def setChavePubica(self, chave_publica):
        self._chave_publica = chave_publica

    def getChavePublica(self):
        return self._chave_publica
    
    def criar_transacao(self, nome_dest: str, valor:float):
        padding_config = config_padding()

        assinatura = assinar_dados()
        transacao = Transacao(self._nome, nome_dest, valor, datetime.now(), assinatura)
        return transacao
    
    #Executa transações
    def executar_transacao(self, transacao: Transacao, saldo ):
        saldo = saldo - transacao._valor
        self._saldo = saldo
        print(f"Executada {transacao._valor}")
        print(f"Resta na sua conta: ")
    
    # Verifica se o saldo á maior que o valor escolhido
    def verificar_transacao(self,  transacao: Transacao):
        """
        Esta função verifica se o saldo é suficiente.

            Args:
                param1 (float): quantidade a ser transferida
                param2 (Usuario): usuário que solicitou a transferência

            Returns:
                bool: True se a operação for bem sucedida, False caso contrário.
            """
        if(transacao._valor > self._saldo):
            print("Seu saldo é insuficiente")
            return False
        else:
            self.executar_transacao(transacao, self._saldo)
            return True
    

#cadastrar usuário:
def cadrastrar_usuario(nome: str):
    chave_privada = criar_chave_privada()
    chave_publica = criar_chave_publica()
    usuario = Usuario(nome, 1000, chave_publica)
        
    print(f"Usuário criado com sucesso {usuario._nome}, sua chave privada é {chave_privada}, seu saldo inicial é {usuario._saldo}")
    return usuario