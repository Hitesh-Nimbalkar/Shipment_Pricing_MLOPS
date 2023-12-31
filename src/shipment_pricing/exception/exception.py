import logging
import sys

class ApplicationException(Exception):
    
    def __init__(self, error_message: Exception, error_details: sys):
        super().__init__(str(error_message))
        self.error_message = self.get_detailed_error_message(error_message=error_message,
                                                             error_details=error_details)

    @staticmethod
    def get_detailed_error_message(error_message: Exception, error_details: sys) -> str:
        _, _, exec_tb = error_details.exc_info()

        line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename

        return f"""
        Error occurred in script: [{file_name}] at 
        line number: [{line_number}] 
        error message: [{error_message}]"""

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.error_message}')"
