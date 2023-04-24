from wtforms import ValidationError


class UniqueEmail:
    def __init__(self, message: str = None) -> None:
        if not message:
            message = "Email is already taken."
        self.message = message

    def __call__(self, form, field):
            raise ValidationError(self.message)
