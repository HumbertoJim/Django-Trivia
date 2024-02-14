class QuestionError(BaseException):
    def __init__(self, message='') -> None:
        super().__init__(message)

class AnswerError(BaseException):
    def __init__(self, message='') -> None:
        super().__init__(message)