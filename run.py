from StardewWikiGetter import StardewWikiGetter
import sqlite3

getter = StardewWikiGetter(StardewWikiGetter.ITEM_PAGE_TITLE)
reactions = getter.get_giftable_item_reactions()

f = open("reactions.txt", "w+")
conn = sqlite3.connect("SDV.db")
c = conn.cursor()

for reaction in reactions:
    f.write(f"{reaction.villager}|||{reaction.item}|||{reaction.reaction}\n")

for reaction in reactions:
    c.execute("INSERT INTO gifts VALUES(?, ?, ?)", (reaction.villager, reaction.item, reaction.reaction))
    
    
f.close()
    
conn.commit()
conn.close()