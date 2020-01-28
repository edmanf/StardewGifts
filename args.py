import argparse
import datetime


description = "Build a database of gifts from the stardew wiki."
parser = argparse.ArgumentParser(description=description)

parser.add_argument(
    "outfile", 
    help="The file to write the database to.")
 
help = "Input file of gift reactions. One on each line, in the " + \
    "NAME|||Item|||Reaction" 
format = "%Y-%m-%d_%H:%M:%S"
timestamp = datetime.datetime.now().strftime(format)
parser.add_argument(
    "-i",
    help= help,
    default=f"SV_Gifts_{timestamp}.db"
    )
    

parser.add_argument(
    "-t",
    help="write to a file instead of a sqlite3 database"
)
    
args = parser.parse_args()

