import socket

def main():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Terhubung ke server.")

        while True:
            message = input("Masukkan pesan: ")
            client_socket.sendall(message.encode('utf-8'))

            if message == 'byebye':
                print("Menutup koneksi.")
                break

            response = client_socket.recv(1024).decode('utf-8')
            print("Jumlah karakter yang diterima dari server:", response)

if __name__ == "__main__":
    main()