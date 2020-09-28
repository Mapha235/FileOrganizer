class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class FilenameAlreadyExistsError(Error):
    """Raised when a file with the same filename already exists in the destination folder."""
    
    def __init__(self):
        super(FilenameAlreadyExistsError, self).__init__()
    

