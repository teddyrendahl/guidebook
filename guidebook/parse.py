"""
Parse the templated Excel Spreadsheet
"""
##############
#  Standard  #
##############
import logging

##############
#  External  #
##############
import xlrd
import pandas

##############
#   Module   #
##############
from .problem import Problem, Boulder
from .errors  import TableNotFoundError

logger = logging.getLogger(__name__)

class ExcelTemplate:
    """
    Excel Template

    Attributes
    ----------
    sheet : xlrd.Sheet
        Sheet object used to find the location of each data table

    table_names : list
        The identifier of each table in the Excel template
    """
    #Names of tables in Excel
    table_names = ['Area Information', 'Boulders', 'Problems']

    def __init__(self, path):
        #Grab and store the first sheet in the xlsx file
        logger.debug("Opening Excel Workbook %s ...", path)
        book = xlrd.open_workbook(path)
        self.path  = path
        self.sheet = book.sheet_by_index(0)

    def find_tables(self):
        """
        Find all of the tables
        
        Returns
        -------
        tables : dict
            Dictionary of each table with the names :attr:`.table_names`
        """
        #Table information
        last_row     = len(self.sheet.col_values(0))
        table_starts = list()
        tables       = list()

        #Find the start of the table
        for table in self.table_names:
            try:
                table_starts.append(self.sheet.col_values(0).index(table))

            #Report an unfound table
            except ValueError as exc:
                raise TableNotFoundError("Unable to find table '{}' in {}"
                                         "".format(table, self.path)) from exc
        #Create tables
        for i, start in enumerate(table_starts):
            #Ignore all subsequent tables
            try:
                footer = last_row - table_starts[i+1]
            #No footer for the last table
            except IndexError:
                footer = 0
            #Find column count
            cols = len([i for i in self.sheet.row(start+1) if i.value])
            #Create table object
            tables.append(TemplatedTable(self.path, start, cols,
                                         footer=footer))
        return dict(zip(self.table_names, tables))



class TemplatedTable:
    """
    Class to parse a generic table of information using xlrd

    Parameters
    ----------
    path : str
        Sheet that holds table information

    start : int
        Header location

    cols :int
        Number of columns to look

    footer : int, optional
        Length of footer to ignore at the end of the file
    """
    _table_id = None

    def __init__(self, path, start, cols, footer=0):
        #Create DataFrame of Excel information
        table = pandas.read_excel(path, skiprows=start,
                                  skip_footer=footer, index_col=0,
                                  header=1, parse_cols=cols-1)
        #Drop emtpy table rows
        self.frame = table[pandas.notnull(table.index)]

    def instantiate_objects(self, cls):
        """
        Instantiate objects from rows in the table
        """
        objs = list()
        #Grab info
        for idx in self.frame.index:
            obj_info = self.frame.loc[idx].to_dict()
            #All keywords should be lowercase
            kwargs = dict((k.lower(), v) for k,v in obj_info.items())
            try:
                objs.append(cls(idx, **kwargs))
            except Exception as exc:
                logger.error("Error loading item %s from spreadsheet", idx)
        return objs
