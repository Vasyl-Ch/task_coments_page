from django.core.validators import RegexValidator

validate_latin_alphanumeric = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    message="Имя пользователя должно содержать только латиницу и цифры.",
)
