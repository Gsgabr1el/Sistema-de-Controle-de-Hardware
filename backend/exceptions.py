class DomainError(Exception):
    status_code = 400
    code = "DOMAIN_ERROR"

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class UnauthorizedError(DomainError):
    status_code = 401
    code = "UNAUTHORIZED"

class NotFoundError(DomainError):
    status_code = 404
    code = "NOT_FOUND"


class BadRequestError(DomainError):
    status_code = 400
    code = "BAD_REQUEST"


class ConflictError(DomainError):
    status_code = 409
    code = "CONFLICT"

