

class Logger:
    """
        Class that provides methods to log warnings and errors.
    """

    @staticmethod
    def warning(self, message):
        print("[Warning] {}".format(message))

    @staticmethod
    def error(self, message):
        print("[Error] {}".format(message))
