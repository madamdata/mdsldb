import mysql.connector, os, re, rich
from rich import print
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.color import Color
from mysql.connector import Error
from functions import rgb, read_query, execute_query, print_raw_query_to_table


class columnStyle():
    def __init__(self, name, style, width=None, ratio=None):
        self.columnname = name
        self.style = style
        self.width = width

class DB_table():
    """ Base class for displaying a table of results"""
    table_name = ''
    cellstyles = {}

    @classmethod
    def fromDB(clss, columns, record_objects):
        db_table = clss()
        db_table.columns = columns
        db_table.objects = record_objects
        db_table.cellstyles = clss.cellstyles
        return db_table

    def printTable(self):
        print(self.objects)


class DB_jobsum_table(DB_table):
    table_name = 'Job Summary'

    cellstyles = {
            'description':{
                'style': Style(color=rgb(185,110,100), bold=True),
                'ratio': 0.12
                },
            'task_description':{
                'style': Style(color=rgb(130,150,210), bold=True),
                'ratio': 0.28
                },
            'jID':{
                'style': Style(color=rgb(130,190,210), bold=True),
                'width': 3
                },
            'clientname': {
                'style': Style(color=rgb(150,200,100),bold=True),
                'with': 7
                },
            'itemname': {
                'style': Style(color=rgb(120,80,200), bold=True),
                'width': 16
                },
            'tags': {
                'style': Style(color=rgb(120,180,100), bold=True),
                },
            'completed': {
                'style': Style(color=rgb(50,200,100), bold=True),
                'width': 2
                },
            'next_task': {
                'style': Style(color=rgb(200,160,150), bold=True),
                'width': 3
                }
            }

    def printTable(self):
        console = Console()
        table = Table(title='Job Summary',
                padding=(0,0),
                expand=True,
                row_styles=(Style(bgcolor=rgb(70,55,65)), Style(bgcolor=rgb(60,45,60)))
                )
        # print(self.cellstyles['jID']['style'])
        for item in self.columns:
            columntitle = item[0]
            try: #if there is a matching entry in cellstyles, use that. otherwise, default to blue
                style = self.cellstyles[columntitle]['style']
            except:
                style = 'blue'

            try:
                width = self.cellstyles[columntitle]['width']
            except:
                width = None

            try:
                ratio = self.cellstyles[columntitle]['ratio']
            except:
                ratio = None

            table.add_column(columntitle, 
                    overflow='fold',
                    no_wrap= True,
                    ratio = ratio,
                    width = width,
                    style = style
                    )

        for record in self.objects:
            #reconstruct record as a list, not a tuple
            recordlist = []
            for item in record:
                recordlist.append(str(item))
            table.add_row(*recordlist)

        console.print(table)
        # print(self.objects)

        
    


