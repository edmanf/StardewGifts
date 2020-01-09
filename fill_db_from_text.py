import sqlite3

file = open("reactions.txt")
reactions = file.readlines()
file.close()


conn = sqlite3.connect("SDV.db")
c = conn.cursor()
c.execute("""CREATE TABLE if not exists gifts
              (villager text, item text, reaction text,
              PRIMARY KEY(villager, item))""")
              
for reaction in reactions:
    name, item, react = reaction.split("|||")
    print(f"name: {name} -- item: {item} -- reaction: {react}")
    c.execute("INSERT INTO gifts VALUES(?, ?, ?)", (name, item, react))
conn.commit()
conn.close()