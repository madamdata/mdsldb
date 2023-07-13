import mysql.connector, os, re, rich
from rich import print
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.color import Color
from mysql.connector import Error
from functions import rgb, read_query, execute_query, print_raw_query_to_table


class DB_table():
    """ Base class for displaying a table of results"""
    table_name = ''

    @classmethod
    def fromDB(clss, record_objects):
        pass
    


