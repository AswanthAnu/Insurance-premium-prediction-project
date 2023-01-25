import os
import sys

class InsuranceException(Exception):
    
    def __init__(self, error_message: Exception, error_detail:sys) -> str:
        super().__init__(error_message) # calling the superclass's init method

        self.error_message = InsuranceException.error_message_detail(error_message, error_detail=error_detail)

    @staticmethod
    def error_message_detail(error_message: Exception, error_detail:sys)->str:
        """
        error: Exception object raise from module
        error_detail: is sys module contains detail information about system execution information.
        """
        _, _, exc_tb = error_detail.exc_info() # getting the traceback object
        
        line_number = exc_tb.tb_frame.f_lineno # getting the line number where exception occurred

        file_name = exc_tb.tb_frame.f_code.co_filename # getting the file name where exception occurred

        # preparing error message
        error_message = f"Error occured python script name [{file_name}]" \
                        f" line number [{line_number}] error message[{Exception}]."


        return error_message # formatting the error message string with file name, line number, and error message

    def __str__(self):
        return InsuranceException.__name__.__str__() # returning the name of the exception class as a string