
import locale

def set_spanish() -> None:
    locale.setlocale(locale.LC_TIME, 'es_MX')

def set_default() -> None:
    locale.setlocale(locale.LC_TIME, '')
