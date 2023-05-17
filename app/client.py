import pickle
import socket
import os

from request import Request, Actions
from response import Response


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

account_actions = """
0. Exit
1. Get current ballance
2. Withdraw money
3. Deposit money
Enter action: """

auth_actions = """
0. Exit
1. Register
2. Login
Enter action: """


def register() -> bool:
    username = input("Enter username: ")
    password = input("Enter password: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    sock.sendall(pickle.dumps(
        Request(
            Actions.REGISTER.value,
            username,
            password,
            content=''
        )
    ))
    resp: Response = pickle.loads(sock.recv(1024))
    sock.close()

    os.environ['USERNAME'] = username
    os.environ['PASSWORD'] = password

    print(resp.message)

    return resp.status


def login() -> bool:
    username = input("Enter username: ")
    password = input("Enter password: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    sock.sendall(pickle.dumps(
        Request(
            Actions.GET_BALANCE.value,
            username,
            password,
            content=''
        )
    ))
    resp: Response = pickle.loads(sock.recv(1024))
    sock.close()

    if resp.status:
        os.environ['USERNAME'] = username
        os.environ['PASSWORD'] = password

        print('Logged in. Your balance:', f'${resp.content}')
    else:
        print(resp.message)

    return resp.status


def get_balance():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    sock.sendall(pickle.dumps(
        Request(
            Actions.GET_BALANCE.value,
            os.getenv('USERNAME'),
            os.getenv('PASSWORD'),
            content=''
        )
    ))
    resp: Response = pickle.loads(sock.recv(1024))
    sock.close()

    if resp.status:
        print('Your balance:', f'${resp.content}')
    else:
        print(resp.message)


def change_balance(top_up: bool):
    amount = input("Enter amount: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    sock.sendall(pickle.dumps(
        Request(
            Actions.DEPOSIT.value if top_up else Actions.WITHDRAW.value,
            os.getenv('USERNAME'),
            os.getenv('PASSWORD'),
            content=amount
        )
    ))
    resp: Response = pickle.loads(sock.recv(1024))
    sock.close()

    print(resp.message)

    if resp.status:
        print('Your balance:', f'${resp.content}')


def main():
    is_auth = False
    while not is_auth:
        auth_action = int(input(auth_actions))

        match auth_action:
            case 0:
                exit(0)
            case 1:
                is_auth = register()
            case 2:
                is_auth = login()

    while True:
        account_action = int(input(account_actions))

        match account_action:
            case 0:
                exit(0)
            case 1:
                get_balance()
            case 2:
                change_balance(top_up=False)
            case 3:
                change_balance(top_up=True)


if __name__ == "__main__":
    main()
