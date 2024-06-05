import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"\nMensagem recebida: {message.decode()}")
        except:
            print("Erro ao receber mensagem.")
            client_socket.close()
            break

def send_messages(client_socket, username):
    while True:
        try:
            message = input(f"{username}: ")
            if message.lower() == 'sair':
                client_socket.close()
                break
            message_with_username = f"{username}: {message}"
            client_socket.send(message_with_username.encode())
        except:
            print("Erro ao enviar mensagem.")
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
