"""
code : meaning

    - 0: no team api id
"""


class TeamException(Exception):

    def __init__(self, code):
        super(TeamException, self).__init__()
        self.code = code

    def get_code(self):
        return self.code
