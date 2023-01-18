class NoEntryPointsFoundError(Exception):
    def __str__(self):
        return "No @entrypoint function found."


class MultipleEntryPointsFoundError (Exception):
    def __str__(self):
        return "Multiple @entrypoint functions found."
