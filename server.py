import argparse
import os
import socket

def list_files(conn, directory='.'):
    parser = argparse.ArgumentParser(description='List files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    args = parser.parse_args()

    files = os.listdir(args.directory)
    files_str = '\n'.join(files)
    conn.sendall(files_str.encode('utf-8'))

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return "File {} telah dihapus.".format(filename)
    else:
        return "File {} tidak ada.".format(filename)

def upload_file(conn, filename):
    with open(filename, 'wb') as f:
        data = conn.recv(1024)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
    print("File {} telah diunggah.".format(filename)) 

def download_file(conn, filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = f.read(1024)
            while data:
                conn.sendall(data)
                data = f.read(1024)
        return "File {} berhasil diunduh.".format(filename)
    else:
        return "File {} tidak ada.".format(filename)

def get_file_size(filename):
    if os.path.exists(filename):
        size_bytes = os.path.getsize(filename)
        return str(size_bytes)
    else:
        return "File {} tidak ada.".format(filename)

def handle_client(conn):
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        command = data.split()
        if command[0] == 'ls':
            list_files(conn, command[1] if len(command) > 1 else '.')
        elif command[0] == 'rm':
            if len(command) > 1:
                response = remove_file(command[1])
            else:
                response = "Penggunaan: rm [namafile]"
            conn.sendall(response.encode('utf-8'))    
        elif command[0] == 'upload':
            if len(command) > 1:
                filename = command[1]
                response = upload_file(conn, filename)
                conn.sendall(response.encode('utf-8'))
            else:
                response = "Penggunaan: upload [namafile]"
            conn.sendall(response.encode('utf-8'))
            if response == "ready":
             continue 
        elif command[0] == 'download':
            if len(command) > 1:
                filename = command[1]
                response = download_file(conn, filename)
            else:
                response = "Penggunaan: download [namafile]"
            conn.sendall(response.encode('utf-8'))
        elif command[0] == 'size':
            if len(command) > 1:
                filename = command[1]
                response = get_file_size(filename)
            else:
                response = "Penggunaan: size [namafile]"
            conn.sendall(response.encode('utf-8'))
        elif command[0] == 'byebye':
            response = "Selamat tinggal!"
            conn.sendall(response.encode('utf-8'))
            conn.close()
            break
        elif command[0] == 'connme':
            response = "Koneksi berhasil dibuat kembali."
            conn.sendall(response.encode('utf-8'))
            continue  
        else:
            response = "Perintah tidak valid."
            conn.sendall(response.encode('utf-8'))

def main():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("Menunggu koneksi...", PORT)

        while True:
            conn, addr = server_socket.accept()
            print('Terhubung dengan', addr)
            handle_client(conn)
            handle_client(conn)

if __name__ == "__main__":
    main()