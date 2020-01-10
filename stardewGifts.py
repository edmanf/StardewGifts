import sqlite3
import argparse
import datetime
from StardewWikiGetter import StardewWikiGetter
from GiftReaction import GiftReaction


def build_items_db(cursor):
    cursor.execute("""CREATE TABLE if not exists items
                      (name text)""")
                      
def build_gifts_db(cursor):
    cursor.execute("""CREATE TABLE if not exists gifts
                      (villager text, item text, reaction text,
                      PRIMARY KEY(villager, item, reaction))""")

def build_villagers_db(cursor):
    cursor.execute("""CREATE TABLE if not exists villagers 
               (name text PRIMARY KEY)""")
    f = open("villagers.txt")
    names = f.readlines()
    for name in names:
        cursor.execute("INSERT INTO villagers VALUES(?)", (name.strip('\n'),))
    f.close()
    
def build_all(cursor):
    build_villagers_db(c)
    build_items_db(c)
    build_gifts_db(c)
    
    
def args():
    description = "Build a database of gifts from the stardew wiki."
    parser = argparse.ArgumentParser(description=description)

    format = "%Y%m%d_%H:%M:%S"
    timestamp = datetime.datetime.now().strftime(format)
    parser.add_argument(
        "-o", 
        help="The file to write the database to.",
        default=f"svgifts_{timestamp}.db")
     
    help = "Input file of gift reactions. One on each line, in the " + \
        "NAME|||Item|||Reaction" 
    parser.add_argument(
        "-i",
        help= help
        )
        

    parser.add_argument(
        "-t",
        help="write to a file instead of a sqlite3 database"
    )
        
    args = parser.parse_args()
    return args
    

if __name__ == "__main__":
    args = args()    
    reactions = list()
    
    if args.i:
        # get gifts from textfile
        f = open(args.i)
        for line in f.readlines():
            name, item, reaction = line.split("|||")
            reactions.append(GiftReaction(name, item, reaction))
    else:
        # get gifts from wiki
        getter = StardewWikiGetter(StardewWikiGetter.ITEM_PAGE_TITLE)
        reactions = getter.get_giftable_item_reactions()
        
    
    if args.t:
        # write to textfile
        f = open(args.o, "w+")
        for reaction in reactions:
            f.write(f"{reaction.villager}|||{reaction.item}|||{reaction.reaction}\n")
            
        f.close()
    else:
        # write to db
        print(args.o)
        conn = sqlite3.connect(args.o)
        c = conn.cursor()
        build_gifts_db(c)
        for reaction in reactions:
            c.execute("INSERT INTO gifts VALUES(?, ?, ?)", (reaction.villager, reaction.item, reaction.reaction))
        
        conn.commit()
        conn.close()
    



    

