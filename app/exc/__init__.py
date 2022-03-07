from werkzeug.exceptions import NotFound, Unauthorized


class PermissionError(Unauthorized):
    ...

class EmptyListError(NotFound): ...