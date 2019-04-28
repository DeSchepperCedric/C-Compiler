

class Logger:
    """
        Class that provides methods to log warnings and errors.
    """

    @staticmethod
    def warning(message):
        print("[Warning] {}".format(message))

    @staticmethod
    def error(message):
        print("[Error] {}".format(message))
