class NotAuthenticated(Exception):
    def __init__(self, message='Not authenticated'):
        self.message = message
        super().__init__(self.message)