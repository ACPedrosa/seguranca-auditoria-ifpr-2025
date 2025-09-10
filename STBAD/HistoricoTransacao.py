"""
    HistoricoTransacao - classe destinada aos atributos e funções referente ao histócio de transações do sistema
    @autor(a): Ana Caroline Pedrosa
    Date: 03/09/2025
"""
from Transacao import Transacao
from datetime import datetime

class HistoricoTransacao(Transacao):
    def __init__(self, remetente: str, destinatario: str, valor: float, data_hora: datetime, assinatura_digital: bytes, estado_assinatura: bool):
        super().__init__(remetente, destinatario, valor, data_hora, assinatura_digital)
        self._estado_assinatura = estado_assinatura

    # Getter e Setter para estado_assinatura
    def get_estado_assinatura(self) -> bool:
        return self._estado_assinatura

    def set_assinatura_digital(self, estado_assinatura: bool):
        self._estado_assinatura = estado_assinatura

