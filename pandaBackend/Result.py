

class Result:
    def __init__(self, data=None, status=True, code=0, message=""):
        self.status = status
        self.code = code
        self.message = message
        self.data = data

    def toDict(self):
        return {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "data": self.data,
        }
