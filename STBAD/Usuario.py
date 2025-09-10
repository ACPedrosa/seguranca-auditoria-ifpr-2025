"""
    Usuário - classe destinada aos atributos e funções do usuário do sistema
    @autor(a): Ana Caroline Pedrosa
    Date: 03/09/2025
"""
from Transacao import Transacao 
from seguranca import *
import os
import json
from datetime import datetime

class Usuario:
    def __init__(self, nome: str, saldo: float, chave_publica):
        self._nome = nome
        self._saldo = saldo
        self._chave_publica = chave_publica
        self._data_criacao = str(datetime.now())

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
        data_hora = datetime.now()

        # Ler a chave privada str(PEM) do usuario, e converter para PEM
        print("Lendo sua chave privada")
        chave_privada = carregar_chave_publica_de_arquivo(self._nome)

        mensagem = f"Remetente: {self._nome}\nDestinatario: {nome_dest}\nValor: {valor:.2f}\nData/Hora: {data_hora}".strip().encode()
        assinatura = assinar_dados(chave_privada, mensagem, padding_config)  

        transacao = Transacao(self._nome, nome_dest, valor, data_hora, assinatura)
        transacao.validar_status(self._chave_publica, assinatura, padding_config)
        
        return transacao
    
    #Executa transações
    def executar_transacao(self, transacao: Transacao, saldo ):
        saldo = saldo - transacao._valor
        self._saldo = saldo
        print(f"\nExecutada {transacao._valor}")
        print(f"Resta na sua conta: {self.getSaldo()}")
    
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
        
    def criar_doc_usuario(self):
        return {
            "Nome": self._nome,
            "Saldo": self._saldo,
            "Chave_Publica": ler_chave_publica_pem_to_str(self._chave_publica),
            "data_criação": self._data_criacao,
        }

    def save_usuario_file(self):
        docUsuario = self.criar_doc_usuario()
        arquivo = "./STBAD/usuarios.json"


        # Se o arquivo existe, lê a lista existente
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                try:
                    usuarios = json.load(f)
                except json.JSONDecodeError:
                    usuarios = []
        else:
            usuarios = []

        if(self._nome not in usuarios):
            # Adiciona a nova transação
            usuarios.append(docUsuario)

            # Escreve toda a lista de volta
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(usuarios, f, ensure_ascii=False, indent=4)

        return
    
#cadastrar usuário:
def cadrastrar_usuario(nome: str):
    usuario = usuarioIsExist(nome)

    if usuario:
        usuario = Usuario(usuario["Nome"], usuario["Saldo"], converter_chave_public_str_to_pem(usuario["Chave_Publica"]))

    if usuario:
        print(f"Usuário logado com sucesso\n{usuario._nome} sua chave privada está salva na pasta ./rsa_keys, seu saldo inicial é {usuario._saldo}")
    else:
        chave_privada = criar_chave_privada()
        save_private_key_file(chave_privada, nome)

        chave_publica = criar_chave_publica(chave_privada)
        usuario = Usuario(nome, 1000, chave_publica)

        usuario.save_usuario_file()
            
        print(f"Usuário criado com sucesso\n{usuario._nome} sua chave privada está salva na pasta ./rsa_keys, seu saldo inicial é {usuario._saldo}")
    return usuario


def usuarioIsExist(nome):
    try:
            with open("./STBAD/usuarios.json", "r", encoding="utf-8") as f:
                usuarios = json.load(f)

            # Filtrar apenas as do usuário
            for u in usuarios:
                if u["Nome"] == nome:
                    return u
            
            return {}
            
    except FileNotFoundError:
        print("Nenhum usuario  encontrado.\n")
    except json.JSONDecodeError:
        print("Erro ao ler usuarios (JSON inválido).\n")
