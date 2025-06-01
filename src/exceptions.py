# Handling Exceptions

import sys

def error_message_detail(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()
    
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    line_number = exc_tb.tb_lineno
    
    error = str(error)
    
    error_message = "Error occured python script name[{0}] line number [{1}] error message [{2}]".format(
        file_name,
        line_number,
        error
    )
    
    # parsing the error
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        #initiating base class
        super().__init__(error_message)
        
        #Extracting the error message
        self.error_message = error_message_detail(
            error_message, error_detail = error_details
        )
        
    def __str__(self):
        return self.error_message