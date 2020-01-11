import sqlite3
import argparse
import datetime
from StardewWikiGetter import StardewWikiGetter
from GiftReaction import GiftReaction
        
def write_reactions_to_db(reactions, filename):
    conn = sqlite3.connect(f"{filename}.db")
    c = conn.cursor()
    build_gifts_db(c)
    
    for reaction in reactions:
        c.execute("INSERT INTO gifts VALUES(?, ?, ?)", (reaction.villager, reaction.item, reaction.reaction))
    
    conn.commit()
    conn.close()
        
def write_reactions_to_textfile(reactions, filename):
    f = open(f"{filename}.txt", "w+")
    for reaction in reactions:
        f.write("{}|||{}|||{}\n".format(
            reaction.villager,
            reaction.item,
            reaction.reaction))
    f.close()

def get_gift_reactions_from_wiki():
    """
        Return a list of gift reactions taken from the stardewvalleywiki
    """
    getter = StardewWikiGetter(StardewWikiGetter.ITEM_PAGE_TITLE)
    return getter.get_giftable_item_reactions()

def get_gift_reactions_from_textfile(filepath):
    """
        Return a list of gift reactions from the given filepath.
        The file must have one reaction per line, each with the 
        format VILLAGER|||ITEM|||REACTION
    """
    reactions = list()
    f = open(filepath)
    for line in f.readlines():
        name, item, reaction = line.split("|||")
        reactions.append(GiftReaction(name, item, reaction))
    return reactions

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

class Args:
    def __init__(self):
        args = self.parse_args()
        self.input_file = args.i
        self.output_filename = args.o
        self.will_write_to_text = args.t
        
    def will_write_to_text(self):
        return self.will_write_to_text
        
    def is_from_input_file(self):
        return True if self.input_file else False
        
    def get_input_filepath(self):
        return self.input_file
        
    def get_output_filename(self):
        return self.output_filename
        
    def parse_args(self):
        description = "Build a database of gifts from the stardew wiki."
        parser = argparse.ArgumentParser(description=description)

        timestamp_format = "%Y%m%d_%H-%M-%S"
        timestamp = datetime.datetime.now().strftime(timestamp_format)
        default_filename_format = f"svgifts_{timestamp}"
        
        parser.add_argument(
            "-o", 
            help = "The file to write to.",
            default = f"{default_filename_format}")
         
        help = "Input file of gift reactions. One on each line, in the " + \
            "NAME|||Item|||Reaction" 
        parser.add_argument(
            "-i",
            help = help)

        parser.add_argument(
            "-t",
            help = "write to a text file instead of a sqlite3 database",
            action="store_true")
            
        args = parser.parse_args()
        return args
        
        
if __name__ == "__main__":
    args = Args()
    reactions = list()
    
    if args.is_from_input_file:
        reactions = get_gift_reactions_from_textfile(
            args.get_input_filepath())
    else:
        reactions = get_gift_reactions_from_wiki()
    
    if args.will_write_to_text:
        write_reactions_to_textfile(reactions, args.get_output_filename())
    else:
        write_reactions_to_db(reactions, args.get_output_filename())