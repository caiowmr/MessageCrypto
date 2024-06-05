import socket
import threading
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

clients = []

# Carrega a chave privada do servidor
with open("private_key.pem", "rb") as key_file:
    private_key = load_pem_private_key(key_file.read(), password=None)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            # Decifra a mensagem recebida
            decrypted_message = private_key.decrypt(
                message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print(f"Recebido: {decrypted_message.decode()}")
            broadcast(decrypted_message, client_socket)
        except Exception as e:
            print(f"Erro: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 56789))
    server.listen(5)
    print('Socket escutando')

    while True:
        client_socket, addr = server.accept()
        print(f'Conexão estabelecida com {addr}')
        clients.append(client_socket)
        client_socket.send('Conexão estabelecida!'.encode())
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
