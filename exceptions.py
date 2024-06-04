from fastapi import HTTPException, status


class RollException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class RollNotAddedInDB(HTTPException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "Рулон не был добавлен в БД, сервис БД недоступен"
