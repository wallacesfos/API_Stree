from werkzeug.exceptions import NotFound

class PermissionError(Exception):
    ...


class NaoEncontradosRegistrosError(NotFound): ...