from urllib.parse import urlparse

from validators.url import url as url_validation_func

MAX_URL_LENGTH = 255
VAL_INCORRECT_MSG = 'Некорректный URL'
VAL_INCORRECT_LEN_MSG = (
    f'Длина url не может превышать {MAX_URL_LENGTH} символов')


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def validate_url(url: str) -> str:
    error = ''
    validated_url = url_validation_func(url)
    if validated_url is not True:
        return VAL_INCORRECT_MSG
    if len(url) > MAX_URL_LENGTH:
        return VAL_INCORRECT_LEN_MSG
    return error
