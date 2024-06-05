import socket
import threading

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Recebido: {message.decode()}")
            broadcast(message, client_socket)
        except:
            break

    # Remove o cliente da lista e fecha a conexão
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
        # Inicia uma nova thread para lidar com a comunicação com o cliente
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    main()
