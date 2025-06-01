# Exercício 1: Cifrando e Decifrando Arquivos com Cabeçalho Personalizado

**Objetivo:**  
Criar um programa em Python capaz de criptografar e descriptografar arquivos, utilizando AES no modo CBC e um cabeçalho de 32 bytes com metadados sobre o arquivo cifrado.

---

## Instruções

### 1. Cabeçalho do Arquivo Cifrado (32 bytes)

O início do arquivo criptografado deve conter um cabeçalho com os seguintes campos:

| Campo         | Tamanho (bytes) | Descrição                                                                 |
|---------------|-----------------|---------------------------------------------------------------------------|
| Identificador | 2               | Deve conter uma sequência fixa, ex: `b'ED'`, para indicar um arquivo cifrado |
| Versão        | 1               | Versão do formato de cabeçalho (ex: `1`)                                  |
| Algoritmo     | 1               | `1` para AES (reservado para futuras extensões com outros algoritmos)     |
| Modo          | 1               | `1` para modo CBC                                                         |
| IV            | 16              | Vetor de inicialização (gerado aleatoriamente na criptografia)           |
| Reserved      | 11              | Reservado para uso futuro (preencher com `0x00`)                          |

---

### 2. Etapas do Programa (Encrypt)

1. Solicitar ao usuário o caminho de um arquivo para criptografar.  
2. Gerar uma chave de 256 bits (pode ser fixa ou pedida ao usuário).  
3. Gerar o IV (Initialization Vector) aleatoriamente.  
4. Criar o cabeçalho conforme especificado.  
5. Criptografar o conteúdo do arquivo usando AES-CBC.  
6. Escrever o cabeçalho + dados criptografados em um novo arquivo.
7. Salvar o arquivo concatenando ".enc" no final do nome do arquivo.

---

### 3. Descriptografia (Decrypt)

1. Ler o cabeçalho do arquivo cifrado.  
2. Verificar se o identificador, versão e algoritmo estão corretos (validação).  
3. Extrair o IV.  
4. Usar a chave (a mesma da criptografia) para decifrar o conteúdo.  
5. Salvar o arquivo original.

---

## Dicas

- Use o pacote `cryptography` com `Cipher`, `algorithms.AES`, `modes.CBC` e `padding.PKCS7`.
- Lembre-se de aplicar e remover o padding adequadamente.
- Para escrever e ler os campos binários, use a biblioteca `struct` ou concatene os bytes com cuidado.
