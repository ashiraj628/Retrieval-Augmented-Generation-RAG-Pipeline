class AppException(Exception):
    status_code: int = 500
    detail: str = "Internal server error."

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        
class AuthenticationError(AppException):
    status_code = 401
    detail = "Authentication failed."


class InvalidTokenError(AuthenticationError):
    detail = "Invalid or expired token."


class InvalidCredentialsError(AuthenticationError):
    detail = "Invalid email or password."


class UserAlreadyExistsError(AppException):
    status_code = 409
    detail = "Email already exists."

class ConversationNotFoundError(AppException):
    status_code = 404
    detail = "Conversation not found."