from typing import Callable

Address = tuple[str, int]


class LogRoller:
    def __init__(self, dice: Callable[[bytes], bytes], remote_addr: Address) -> None:
        self.dice_roller = dice
        self.remote_addr = remote_addr

    def __call__(self, request: bytes) -> bytes:
        print(f"Receiving {request!r} from {self.remote_addr}")
        dice_roller = self.dice_roller
        response = dice_roller(request)
        print(f"Sending {request!r} to {self.remote_addr}")
        return response
