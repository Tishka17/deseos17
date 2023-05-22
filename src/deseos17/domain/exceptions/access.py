from .base import DomainError


class AuthenticationError(DomainError):
    pass


class AccessDenied(DomainError):
    pass
