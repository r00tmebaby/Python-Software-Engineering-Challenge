import re


def get_chars_within_range(from_decimal: int, to_decimal: int) -> list:
    """

    Ref: https://www.rapidtables.com/code/text/ascii-table.html
    Return ASCII characters within a decimal range

    """

    return [chr(i) for i in range(from_decimal, to_decimal)]


def is_valid_email(email: str) -> bool:
    """ Checks whether the email is valid """
    import validators
    return validators.email(email)


def is_valid_password(password: str) -> bool:
    """ Checks whether the password is valid

        Password should contain at least:
        1 - One of the special characters: ( $ & ! # @ ? )
        1 - Capital Letter
        1 - Lowercase Letter
        1 - Number

    """
    required_special = "$&!#@?"

    return \
        len(password) >= 6 \
        and any(char.isdigit() for char in password) \
        and any(char.isupper() for char in password) \
        and any(char.islower() for char in password) \
        and re.search(f"[{required_special}]", password)
