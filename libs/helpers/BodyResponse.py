from http import HTTPStatus

class BodyResponse:
    def __init__(self, status_code: HTTPStatus, data: list) -> None:
        self.status: str = status_code.phrase
        self.code: int = status_code.value
        self.message: str = status_code.description
        self.data: list = data