from werkzeug.exceptions import NotFound


class PermissionError(Exception):
    ...

class EmptyListError(NotFound): ...