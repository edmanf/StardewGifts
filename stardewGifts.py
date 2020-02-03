import sqlite3
import argparse
import datetime
from StardewGifts.WikiGetter import WikiGetter
from StardewGifts.GiftReaction import GiftReaction
from StardewGifts.SVGDatabase import SVGDatabase

def main():
    args = Args()
    reactions = list()
    
    if args.is_from_input_file():
        reactions = get_gift_reactions_from_textfile(
            args.get_input_filepath())
    else:
        reactions = get_gift_reactions_from_wiki()
    
    if args.will_write_to_text():
        write_reactions_to_textfile(reactions, args.get_output_filename())
    else:
        db = SVGDatabase(args.get_output_filename())
        db.write_reactions(reactions)
        
        
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
    getter = WikiGetter(WikiGetter.ITEM_PAGE_TITLE)
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

class Args:
    def __init__(self):
        args = self.parse_args()
        self.input_file = args.i
        self.output_filename = args.o
        self.write_to_text = args.t
        
    def will_write_to_text(self):
        return self.write_to_text
        
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
    main()