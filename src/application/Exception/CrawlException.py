class NoDataException(Exception):
    def __init__(self, code):
        super(NoDataException, self).__init__()
        self.code = code

    def get_code(self):
        return self.code
