import mysql.connector, os, re, rich
from rich import print
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.color import Color
from mysql.connector import Error
from functions import rgb, read_query, execute_query, print_raw_query_to_table


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
    def fromDict(clss, inputdict, connection):
        """
            from Dictionary
        """ 
        db_dict = clss()
        try:
            fields = read_query(connection, "DESCRIBE {};".format(clss.table_name))
        except:
            pass
        for item in fields:
            fieldname = item[0]
            fieldtype = item[1] 
            try:
                db_dict[fieldname] = (inputdict[fieldname], fieldtype)
            except KeyError: #inputDict doesn't have this key
                db_dict[fieldname] = (None, fieldtype)
            
        return db_dict

    @classmethod
    def byID(clss, idnum, connection):
        """ create new instance by reading from a record. 
            To be called by subclasses only, using the class variable clss.id_string
        """ 
        query = "SELECT * from {} WHERE {} LIKE {} LIMIT 1;".format(clss.table_name, clss.id_string, idnum)
        columns = read_query(connection, "DESCRIBE {};".format(clss.table_name))
        queryreply = read_query(connection, query)
        if queryreply: 
            record = queryreply[0]
        else:
            return None
        db_dict=clss.fromDB(columns, record)
        return db_dict

    @classmethod
    def byField(clss, fieldname, fieldval, connection):
        """ 
            create new instance by reading from a record using an arbitrary field. 
            will only create an instance from the FIRST RESULT of that query. 
            To be called by subclasses only. 
        """ 
        query = "SELECT * from {} WHERE {} LIKE '%{}%' LIMIT 1;".format(clss.table_name, fieldname, fieldval)
        print(query)
        columns = read_query(connection, "DESCRIBE {};".format(clss.table_name))
        queryreply = read_query(connection, query)
        if queryreply: 
            record = queryreply[0]
        else:
            return None
        db_dict=clss.fromDB(columns, record)
        return db_dict

    def __init(self, **kwargs):
        self.id = None

    def generateCreateString(self):
        fieldstring = ''
        valstring = ''
        for key in self:
            # get keys, values and types
            val = self[key][0]
            valtype = str(self[key][1])
            # add quotations to text data types
            if val:
                if 'text' in valtype or 'varchar' in valtype:
                    # put single quotes around strings
                    # val = val.replace("'", "\\'").replace('"', '\\"')
                    val = '\'{}\''.format(val)
                fieldstring = fieldstring + '{},'.format(str(key))
                valstring = valstring + '{},'.format(str(val))
        fieldstring = fieldstring[:-1] #remove final comma
        valstring = valstring[:-1]
        string = "INSERT INTO {} ({}) VALUES ({})".format(self.__class__.table_name, fieldstring, valstring)
        # string = string[:-2] #remove final comma and space
        # self.id = 99
        return string

    def generateUpdateString(self):
        string = 'UPDATE {} SET '.format(self.__class__.table_name)
        for key in self:
            # get keys, values and types
            val = self[key][0]
            valtype = str(self[key][1])
            # add quotations to text data types
            if val:
                if 'text' in valtype or 'varchar' in valtype:
                    val = val.replace("'", "\\'").replace('"', '\\"')
                    val = '\'{}\''.format(val)
                string = string + '{} = {}, '.format(str(key), str(val))

        string = string[:-2] #remove final comma and space
        # self.id = 99
        string = string + ' WHERE {} like {} LIMIT 1;'.format(self.__class__.id_string, str(self.id))
        return string

    def setid(self, idnum):
        if idnum.__class__ == str:
            try:
                self.id = int(idnum)
            except AttributeError as err:
                print("Id is not a recognized number.")

    def printToTable(self):
        table = Table(title='task' + str(self.id), 
                padding=(0,0),expand=True, 
                row_styles=(Style(bgcolor=rgb(70,55,65)), 
                Style(bgcolor=rgb(60,45,60)))
                )
        for item in self:
            table.add_column(item, overflow='fold', width=None)
        table.add_row(*(str(self[x][0]) for x in self))
        print(table)



class DB_client(DB_Dict):
    id_string = 'client_ID'
    table_name = 'clients'
    """class encapsulating client data"""
    def __init__(self, **kwargs):
        pass



class DB_task(DB_Dict):
    id_string = 'task_ID'
    table_name = 'tasks'
    """class encapsulating task data and functions"""
    def __init(self, **kwargs):
        pass

    def delete_task(self, connection):
        query = "DELETE from tasks WHERE task_ID LIKE "+ str(self.id) + " LIMIT 1;"
        jobid = self['job_ID'][0]
        execute_query(connection, query)
        print("Deleting task {}.".format(str(self.id)))
        if jobid:
            setnexttaskquery = 'CALL setnexttask({});'.format(jobid)
            execute_query(connection, setnexttaskquery)

    def taskdone(self, connection):
        query = "UPDATE tasks SET completed = 1 WHERE task_ID = {}".format(str(self.id))
        jobid = self['job_ID'][0]
        execute_query(connection, query)
        print("Task {} completed.".format(str(self.id)))
        if jobid:
            setnexttaskquery = 'CALL setnexttask({});'.format(jobid)
            execute_query(connection, setnexttaskquery)

                    

class DB_job(DB_Dict):
    id_string = 'job_ID'
    table_name = 'jobs'
    """class encapsulating job data and functions"""


    def __init(self, **kwargs):
        pass

class DB_income(DB_Dict):
    id_string = 'Transaction_ID'
    table_name = 'income'
    """class encapsulating an income entry"""
    def __init(self, **kwargs):
        pass
