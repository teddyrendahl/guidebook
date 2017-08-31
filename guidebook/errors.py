"""
Contains all exceptions specific to `guidebook`
"""

class TableNotFoundError(Exception):
    """
    Exception raised when excepted data table is not found in given Excel
    document
    """
