import socket
import threading
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Carrega a chave pública do servidor
with open("public_key.pem", "rb") as key_file:
    public_key = load_pem_public_key(key_file.read())

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"\nMensagem recebida: {message.decode()}")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            client_socket.close()
            break

def send_messages(client_socket, username):
    while True:
        try:
            message = input(f"{username}: ")
            if message.lower() == 'sair':
                client_socket.close()
                break
            message_with_username = f"{username}: {message}".encode()
            # Cifra a mensagem antes de enviar
            encrypted_message = public_key.encrypt(
                message_with_username,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            client_socket.send(encrypted_message)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            client_socket.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 56789))
    username = input("Digite seu nome de usuário: ")
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(client, username))
    send_thread.start()
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":
    main()
