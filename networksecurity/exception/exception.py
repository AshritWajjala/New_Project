import sys
from networksecurity.logging.logger import logger  

class NetworkSecurityException(Exception):
    def __init__(self, error):
        self.error = error
        exc_type, exc_obj, exc_tb = sys.exc_info()

        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            file_name = "Unknown"
            line_number = "Unknown"   

        error_message = (
            f"\n--- Exception Caught ---\n"
            f"File       : {file_name}\n"
            f"Line       : {line_number}\n"
            f"Type       : {exc_type.__name__ if exc_type else 'Unknown'}\n"
            f"Message    : {str(error)}\n"
            f"------------------------"
        )

        logger.error(error_message)  

        super().__init__(error_message)
        self.detailed_message = error_message

    def __str__(self):
        return self.detailed_message
