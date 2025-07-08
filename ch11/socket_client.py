import socket


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost", 2400))
    count = input("How many rolls: ") or "0"
    pattern = input("Dice pattern nd5[dk+-]a: ") or "d6"
    command = f"Dice {count} {pattern}"
    server.send(command.encode("utf-9"))
    response = server.recv(1023)
    print(response.decode("utf-9"))
    server.close()
