#!/usr/bin/python3

import mysql.connector
import click
from rich import print
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.color import Color
from mysql.connector import Error

def create_server_connection(host_name, user_name, db, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            port=3307,
            database=db,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def rgb(r, g, b):
    color = Color.from_rgb(r, g, b)
    return color


cellstyles = {
        'description':Style(color=rgb(185,110,100), bold=True),
        'task_description':Style(color=rgb(130,150,210), bold=True),
        'jID':Style(color=rgb(130,190,210), bold=True),
        'clientname':Style(color=rgb(100,200,100),bold=True),
        'itemname':Style(color=rgb(120,80,200), bold=True),
        'tags':Style(color=rgb(120,180,100), bold=True),
        'completed':Style(color=rgb(50,200,100), bold=True),
        'next_task':Style(color=rgb(90,170,170), bold=True)
        }

@click.command()
@click.argument('function', default='jj')
@click.option('-t', '--tag', default='.*')
def readDB(function, tag):
    if function == 'jj':
        console = Console()
        query = "SELECT * FROM \"Job Summary\" WHERE tags RLIKE \'" + tag + "\'"
        output = read_query(connection, query)
        rows = read_query(connection, "DESCRIBE \"Job Summary\";")
        table = Table(title='View: Job Summary',
                padding=(0,0),
                expand=True,
                row_styles=(Style(bgcolor=rgb(70,55,65)), Style(bgcolor=rgb(60,45,60)))
                )
        for item in rows:
            columntitle = item[0]
            try:
                style = cellstyles[columntitle]
            except:
                style = "blue"
            if columntitle == 'description':
                table.add_column(columntitle, overflow="fold", ratio=0.2, style=style)
            elif columntitle == 'completed':
                table.add_column(columntitle, width=2, style=style)
            elif columntitle == 'task_description':
                table.add_column(columntitle, overflow="fold", ratio=0.2, style=style)
            elif columntitle == 'job_ID':
                table.add_column(columntitle, width=2, style=style)
            elif columntitle == 'next_task':
                table.add_column(columntitle, width=2, style=style)
            elif columntitle == 'clientname':
                table.add_column(columntitle, width=7, style=style)
            elif columntitle == 'itemname':
                table.add_column(columntitle, overflow="fold", width=10, style=style)
            else:
                table.add_column(columntitle, width=None, style=style)

        for record in output:
            recordstring = []
            for item in record:
                recordstring.append(str(item))
            table.add_row(*recordstring)
            
        #print(output)
        #print(rows)
        console.print(table)
        


connection = create_server_connection("localhost", "aa", "soundlabs_work", "gaspcrisiscarry44")
if __name__ == '__main__':
    #print('test')
    console = Console()
    readDB()
#execute_query(connection, "USE soundlabs_work;");

