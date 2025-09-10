"""
    Transacao - classe destinada aos atributos e funções das transações do sistema
    @autor(a): Ana Caroline Pedrosa
    Date: 03/09/2025
"""

from datetime import datetime
import json
import base64

class Transacao:
    def __init__(self, remetente: str, destinatario: str, valor: float, data_hora: datetime, assinatura_digital: bytes):
        self._remetente = remetente
        self._destinatario = destinatario
        self._valor = valor
        self._data_hora = data_hora
        self._assinatura_digital = assinatura_digital

    # Getter e Setter para remetente
    def get_remetente(self) -> str:
        return self._remetente

    def set_remetente(self, remetente: str):
        self._remetente = remetente

    # Getter e Setter para destinatario
    def get_destinatario(self) -> str:
        return self._destinatario

    def set_destinatario(self, destinatario: str):
        self._destinatario = destinatario

    # Getter e Setter para valor
    def get_valor(self) -> float:
        return self._valor

    def set_valor(self, valor: float):
        self._valor = valor

    # Getter e Setter para data_hora
    def get_data_hora(self) -> datetime:
        return self._data_hora

    def set_data_hora(self, data_hora: datetime):
        self._data_hora = data_hora

    # Getter e Setter para assinatura_digital
    def get_assinatura_digital(self) -> bytes:
        return self._assinatura_digital

    def set_assinatura_digital(self, assinatura_digital: bytes):
        self._assinatura_digital = assinatura_digital
    
    def criar_doc_transacao(self):
        return {
            "remetente": self._remetente,
            "destinatario": self._destinatario,
            "valor": self._valor,
            "data_hora": self._data_hora.strftime('%Y-%m-%d %H:%M:%S'),
            "assinatura_digital": base64.b64encode(self._assinatura_digital).decode('utf-8')
    }

    def log_transacao(transacao, arquivo='log_transacoes.json'):
        with open(arquivo, 'a') as f:
            json.dump(transacao.criar_doc_transacao(), f)
            f.write('\n')

    