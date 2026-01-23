from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator:
    def __init__(self, message: str=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value: str) -> None:
        self.__message = value or "Username may contain only letters, numbers and underscores."

    def __call__(self, value: str) -> None:
        if not value.replace('_', '').isalnum():
            raise ValidationError(self.message)