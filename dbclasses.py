import mysql.connector, os, re
from mysql.connector import Error

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
    print(len(taskrecord))
    if len(taskrecord) > 0:
        for item in taskrecord:
            table.add_row(*(str(x) for x in item))
    return table



class DB_Dict(dict):
    """ Base dict inherited class for MDSL database """
    id_string = None
    table_name = None
    @classmethod
    def fromDB(clss, columndata, data):
        db_dict = clss()
        db_dict.columndata = columndata
        # print(columndata)
        for index, col in enumerate(columndata):
            colname = col[0]
            coltype = col[1]
            db_dict[colname] = (data[index], coltype) 
        id_val = db_dict[clss.id_string][0]
        db_dict.id = id_val
        return db_dict

    @classmethod
    def byID(clss, idnum, connection):
        query = "SELECT * from {} WHERE {} LIKE {} LIMIT 1;".format(clss.table_name, clss.id_string, idnum)
        columns = read_query(connection, "DESCRIBE {};".format(clss.table_name))
        taskrecord = read_query(connection, query)[0]
        db_dict=clss.fromDB(columns, taskrecord)
        return db_dict

    def __init(self, **kwargs):
        self.id = None

    def generateUpdateString(self):
        string = 'UPDATE {} SET '.format(self.__class__.table_name)
        for key in self:
            # get keys, values and types
            val = self[key][0]
            valtype = str(self[key][1])
            # add quotations to text data types
            if val:
                if 'mediumtext' in valtype or 'varchar' in valtype:
                    val = '\'{}\''.format(val)
                string = string + '{} = {}, '.format(str(key), str(val))

        string = string[:-2] #remove final comma and space
        string = string + ' WHERE {} like {} LIMIT 1;'.format(self.__class__.id_string, str(self.id))
        return string

    def setid(self, idnum):
        if idnum.__class__ == str:
            try:
                self.id = int(idnum)
            except AttributeError as err:
                print("Id is not a recognized number.")

class DB_Client(DB_Dict):
    """class encapsulating client data"""
    def __init__(self, **kwargs):
        pass



class DB_task(DB_Dict):
    id_string = 'task_ID'
    table_name = 'tasks'
    """class encapsulating task data and functions"""
    def __init(self, **kwargs):
        pass
                    

class DB_job(DB_Dict):
    """class encapsulating job data and functions"""
    def __init(self, **kwargs):
        pass

class DB_income(DB_Dict):
    """class encapsulating an income entry"""
    def __init(self, **kwargs):
        pass
            
