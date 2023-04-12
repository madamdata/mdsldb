class DB_Dict(dict):
    """ Base dict inherited class for MDSL database """

    @classmethod
    def fromDB(clss, columnnames, data):
        db_dict = clss()
        for index, colname in enum(columnnames):
            d_dict[colname] = data[index] 
        return db_dict

    def __init(self, **kwargs):
        self.id = None

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
            
