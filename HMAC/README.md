# HMAC para esteção metereológica

Este projeto simula uma estação meteorológica que coleta dados climáticos (temperatura, umidade, pressão, entre outros) e os envia para um servidor central com autenticação e integridade garantidas usando HMAC (Hash-based Message Authentication Code).

## Objetivo

Garantir a **autenticidade** e **integridade** das mensagens enviadas pela estação meteorológica para o servidor central, utilizando técnicas de criptografia com HMAC (SHA-256).

---

## Funcionalidades

### Geração de Mensagem Autenticada

* Recebe os dados da estação e uma chave secreta.
* Gera um HMAC usando o algoritmo SHA-256.
* Retorna a mensagem com o HMAC anexado.

### Validação da Mensagem no Servidor

* Recebe a mensagem com o HMAC e a chave secreta.
* Calcula o HMAC localmente e compara com o fornecido.
* Retorna `True` se a mensagem for válida, `False` caso contrário.

---

## Exemplo de Uso

```python
# Dados da estação 
dados = {
    "temperatura": 25.3,
    "umidade": 60.2,
    "pressao": 1013.2,
}

chave_secreta = b"chocolate"

# Geração da mensagem autenticada
mensagem_autenticada = autenticar_mensagem(dados, chave_secreta)

# Validação da mensagem no servidor
validacao = validar_mensagem(mensagem_autenticada, chave_secreta, salt)

print("Mensagem válida?", validacao)
```

---

## Estrutura das Funções

`autenticar_mensagem(dados: dict, chave: bytes) `

Gera o HMAC com base nos dados e retorna um dicionário com os dados e o hash.

`validar_mensagem(mensagem, senha, salt) -> bool`

Recebe a mensagem e verifica se o HMAC bate com os dados.

---

## Tecnologias Utilizadas

* Python 3.12.1
* `hashlib` (SHA-256)
* `hmac`

---

## ✍️ Autor
    Ana Caroline Pedrosa

