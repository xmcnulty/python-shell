class ExitException(Exception):
    """Exception raised to signal shell exit."""
    def __init__(self, exit_code: int = 0):
        self.exit_code = exit_code
        super().__init__(f"Exit with code {exit_code}")