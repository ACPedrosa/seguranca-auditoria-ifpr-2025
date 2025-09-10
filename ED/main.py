from cript_msg import read_file, create_key, create_iv, encrypt_aes, create_header, save_file
import os

# === Main ===
arquivo = input("Digite o caminho do seu arquivo: ")
if not os.path.isfile(arquivo):
    print("Arquivo não encontrado.")
else:
    arqBin = read_file(arquivo)
    chave = create_key()
    iv = create_iv()
    enc = encrypt_aes(chave, iv, arqBin)
    header = create_header(iv)
    save_file(header, enc)