import mysql.connector, os, re, rich
from rich import print
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.color import Color
from mysql.connector import Error

def rgb(r, g, b):
    color = Color.from_rgb(r, g, b)
    return color

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def print_raw_query_to_table(connection, querystring):
    """
    Print arbitrary SQL query (read only)
    """
    tablenamematch = re.search(r"(?i)FROM (\".*\"|[^\s\"]*)", querystring)
    if tablenamematch:
        tablename = tablenamematch.group(1)
        print(tablename)
    else:
        print("No such table.")
        return None
    table = Table(title='query result',
            padding=(0,0),
            expand=True,
            row_styles=(Style(bgcolor=rgb(70,55,65)), Style(bgcolor=rgb(60,45,60)))
            )
    query = querystring
    columns = read_query(connection, "DESCRIBE " + tablename + " ;")
    for item in columns:
        columntitle = item[0]
        table.add_column(columntitle, overflow='fold', width=None)
    taskrecord = read_query(connection, query)
    # print(len(taskrecord))
    if len(taskrecord) > 0:
        for item in taskrecord:
            table.add_row(*(str(x) for x in item))
    return table
