import mysql.connector, os, re, rich
from rich import print
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.theme import Theme
from rich.color import Color
from rich.highlighter import RegexHighlighter
from mysql.connector import Error
from functions import rgb, read_query, execute_query, print_raw_query_to_table


class mdsl_highlighter(RegexHighlighter):
    base_style = "highlight."
    highlights = [
            r"(?P<w4>w4.*)",
            r"(?P<r2>r2.*)",
            r"(?i)(?P<build>build)"
            ]

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

    def printTable(self, options):
        print(self.objects)


class DB_jobsum_table(DB_table):
    table_name = 'Job Summary'

    cellstyles = {
            'description':{
                'style': Style(color=rgb(185,110,100), bold=False),
                'ratio': 0.12
                },
            'task_description':{
                'style': Style(color=rgb(180,165,210), bold=False),
                'ratio': 0.28
                },
            'jID':{
                'style': Style(color=rgb(130,190,210), bold=False),
                'width': 3
                },
            'clientname': {
                'style': Style(color=rgb(150,180,40),bold=False),
                'with': 7
                },
            'itemname': {
                'style': Style(color=rgb(120,80,200), bold=True),
                'width': 16
                },
            'tags': {
                'style': Style(color=rgb(130,180,135), bold=False),
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

    def printTable(self, options):
        #set highlights
        theme = Theme({
            "highlight.w4": Style(color=rgb(120,120,120),bold=False, italic=True),
            "highlight.r2": Style(color=rgb(110,180,180), bgcolor=rgb(80,70,80),bold=True),
            # "highlight.build": Style(color=rgb(180,110,180),bold=True),
            })
        console = Console(highlighter = mdsl_highlighter(), theme = theme)
        table = Table(title='Job Summary',
                padding=(0,0),
                expand=True,
                highlight=True,
                row_styles=(Style(bgcolor=rgb(60,45,55)), Style(bgcolor=rgb(50,35,50))),
                border_style=Style(color=rgb(80,70,90))
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
                    no_wrap= not options['verbose'],
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

        
    


