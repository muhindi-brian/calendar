class ValidationError(Exception):
    """
    docstring
    """

    def __init__(self, error_msg: str, status_code: int):
        """
        docstring
        """
        super().__init__(error_msg)
        self.status_code = status_code
        self.error_msg = error_msg
