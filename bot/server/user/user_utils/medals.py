from header import userDB


class Medals():
    user_id: int
    _message: int


    def __init__(self, user_id) -> None:
        self.user_id = user_id

    
    def get_message(self) -> str:
        self._set_message(

        )

    
    def _set_message(self, text):
        self._message = text