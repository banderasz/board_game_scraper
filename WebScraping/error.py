class BoardGameNotFoundError(Exception):
    def __init__(self, message: str = "Board game is not found"):
        super().__init__(message)
