import sqlite3

class SVGDatabase:
    DEFAULT_GIFT_TABLE_NAME = "gifts"
    DEFAULT_ITEM_TABLE_NAME = "items"
    DEFAULT_ITEM_ATTRIBUTES_TABLE_NAME = "item_attributes"
    
    
    def __init__(self, 
        database_path, 
        gift_table_name = self.DEFAULT_GIFT_TABLE_NAME,
        item_attributes_table_name = self.DEFAULT_ITEM_ATTRIBUTES_TABLE_NAME):
        
        self.gift_table_name = gift_table_name
        self.item_attributes_table_name = item__attributes_table_name
        
        self.database_path = database_path
        self.cursor = self.get_cursor()
        self.build_all()
    
    def write_reactions(self, reactions):
        statement = "INSERT INTO {} VALUES(?, ?, ?)" \
            .format(self.item_table_name)
        args = [(x.villager, x.item, x.reaction) for x in reactions]
        self.write_list(statement, args)
        
    def write_items(self, items):
        statement = "INSERT INTO {} VALUES(?, ?, ?)" \ 
            .format(self.gift_table_name)
        args = [(x.name, x.source, x.season) for x in items]
        self.write_list(statement, args)
        
    def write_item_attributes(self, items):
        statement = "INSERT INTO {} VALUES(?, ?, ?)" \ 
            .format(self.item__attributes_table_name)
            
        args = []
        for item in items:
            for attribute in item.attributes:
                for value in item.attributes[attribute]:
                    args.append(item.name, attribute, value) 
        self.write_list(statement, args)
                
        
    def write_list(self, statement, args):
        """ Executes the given statement with every argument in 
        the args list. """
        
        for arg in args:
            self.cursor.execute(statement, args)
        
    def get_cursor(self):
        self.conn = sqlite3.connect(f"{filename}.db")
        return conn.cursor()
        
    def commit(self):
        self.conn.commit()
        self.conn.close()
        
    def build_items_db(cursor):
        cursor.execute("""CREATE TABLE if not exists {}(
                        name TEXT PRIMARY KEY NOT NULL, 
                        source TEXT NOT NULL,
                        season TEXT NOT NULL)""" \ 
                        .format(self.item_table_name))
                      
    def build_gifts_db(cursor):
        cursor.execute("""CREATE TABLE if not exists {}(
                            villager TEXT NOT NULL, 
                            item TEXT NOT NULL, 
                            reaction TEXT NOT NULL,
                            PRIMARY KEY(villager, item))""" \ 
                            .format(self.gift_table_name))
                            
    def build_item_attributes_db(cursor):
        cursor.execute("""CREATE TABLE if not exists {}(
                            item TEXT NOT NULL, 
                            attribute TEXT NOT NULL,
                            value TEXT NOT NULL
                            PRIMARY KEY(item, attribute, value))""" \
                            .format(self.item_attributes_table_name))
        
    def build_all():
        build_item_attributes_db()
        build_gifts_db()