import pickle

from request import Actions, Request
from response import Response, Messages
from storage import Storage, UserAlreadyExists


class Handler:
    def __init__(self, data: bytes):
        self._data = data
        self._storage = Storage()

    def execute(self) -> bytes:
        rq: Request = pickle.loads(self._data)

        if rq.action == Actions.REGISTER.value:
            response = self._perform_register_action(rq)
        elif not self._storage.authenticate(rq.username, rq.password):
            response = Response(
                status=False,
                message=Messages.INVALID_CREDENTIALS.value,
                content=''
            )
        else:
            response = self._perform_balance_action(rq)

        return pickle.dumps(response)

    def _perform_register_action(self, rq: Request) -> Response:
        try:
            self._storage.create_user(rq.username, rq.password)
            return Response(
                status=True,
                message=Messages.REGISTERED.value,
                content=''
            )
        except UserAlreadyExists:
            return Response(
                status=False,
                message=Messages.USER_ALREADY_EXISTS.value,
                content=''
            )

    def _perform_balance_action(self, rq: Request) -> Response:
        balance = self._storage.get_balance(rq.username)

        match rq.action:
            case Actions.GET_BALANCE.value:
                return Response(
                    status=True,
                    message=Messages.PERFORMED.value,
                    content=str(balance)
                )
            case Actions.WITHDRAW.value:
                future_balance = balance - int(rq.content)

                if future_balance < 0:
                    return Response(
                        status=False,
                        message=Messages.BALANCE_TOO_LOW.value,
                        content=str(balance)
                    )
                else:
                    self._storage.update_balance(rq.username, future_balance)
                    return Response(
                        status=True,
                        message=Messages.BALANCE_UPDATED.value,
                        content=str(future_balance)
                    )
            case Actions.DEPOSIT.value:
                future_balance = balance + int(rq.content)

                self._storage.update_balance(rq.username, future_balance)
                return Response(
                    status=True,
                    message=Messages.BALANCE_UPDATED.value,
                    content=str(future_balance)
                )
