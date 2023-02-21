# exceptions.py
class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ParserFindUrlException(Exception):
    """Вызывается, когда парсер не может найти страницу."""
    pass
