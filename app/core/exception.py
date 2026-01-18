class BaseAppException(Exception):
    """Base class for all custom app exceptions"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DatabaseException(BaseAppException):
    """Raised when a database operation fails"""
    pass

class ValidationException(BaseAppException):
    """Raised when user input or business logic fails validation"""
    pass

class UnauthorizedException(BaseAppException):
    """Raised when a user is not authorized"""
    pass