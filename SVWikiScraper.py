import bs4
from urllib.request import urlopen
from urllib.parse import urljoin
import sqlite3

global SCRAPE_COUNTER, SCRAPE_LIMIT, LOG_PROGRESS
LOG_PROGRESS = True # Enable the printing of messages to track progress
SCRAPE_COUNTER = 0
SCRAPE_LIMIT = 10000 # Limit the number page opens for bandwidth



def scrape_villager_names():
    """ Returns a list of villager names. """
    url="https://stardewvalleywiki.com/Villagers"
    
    page = urlopen(url)
    soup = bs4.BeautifulSoup(page.read(), features="html.parser")
    names = [gt.text.strip('\n') for gt in soup.find_all(class_="gallerytext")]
    return names
    
def write_villager_names_to_file(names, file_path):
    """
        Writes the list of names to a file specified by file_path. Will create
        a file if does not exist. Names are seperated by newlines.
    """
    f = open(file, "w+")
    f.writelines("{}\n".format(name) for name in names)
    f.close()
    
def scrape_items_to_db():
    """
        Returns a list of items
    """
    base = "https://stardewvalleywiki.com/"
    path = "Category:Items"
    
    item_links = get_item_links(urljoin(base, path))
    gift_reactions = get_giftable_item_reactions_from_links(item_links)
    write_gift_reactions_to_db(gift_reactions)
    
    
def get_item_links(url):
    """ Returns a set of item urls from this url and its sub-categories
    
    An item link is considered any link in the main content body of the
    page at the given url that is not a category link. The items from
    the sub-categories of the given url will also be returned as part
    of the set.
    
    Keyword arguments:
    url -- the url should be a category link from the stardew wiki
        ex: https://stardewvalleywiki.com/Category:Animal_Products
    
    """
    global SCRAPE_COUNTER
    if SCRAPE_COUNTER >= SCRAPE_LIMIT:
        print("Limit reached! " + url + " skipped!")
        return []
    if LOG_PROGRESS:
        print("Opening----" + url)
    page = urlopen(url)
    
    SCRAPE_COUNTER += 1
    soup = bs4.BeautifulSoup(page.read(), features="html.parser")
    groups = soup.find_all(class_="mw-category-group")
    end_links = set()
    
    for group in groups:
        links = group.find_all("a")
        for link in links:
            path = link["href"]
            if "Category:" in path:
                end_links = end_links.union(get_item_links(urljoin(url, path)))
            else:
                end_links.add(urljoin(url, path))
                
    if LOG_PROGRESS:
        print(url + " scraped!")
    return end_links
    
    
def get_giftable_item_reactions(item_links):
    """
        Return a list of GiftReactions scraped from the given list of
        urls item_links.
    """
    if LOG_PROGRESS:
        print("Writing " + str(len(item_links)) + " items to db...")
        
    reactions = []
    for link in item_links:
        if LOG_PROGRESS:
            print("Opening---" + link)
        soup = bs4.BeautifulSoup(urlopen(link).read(), features="html.parser")
        
        item = soup.find(id="firstHeading").text.strip("\n ")
        
        gift_header = soup.find(id="Gifting")
        if not gift_header:
            # Item is not giftable
            continue

        rows = gift_header.parent.find_next("table").find_all("tr")
        table_name = rows[0].text.strip("\n ")
        if table_name != "Villager Reactions":
            continue
        
        for row in rows[1:]:
            reaction = row.find("th").text.strip("\n ")
            villagers = [x.text.strip("\n ") for x in row.find_all("div")]
            for villager in villagers:
                reactions.append(GiftReaction(villager, item, reaction))
                
    return gift_reactions
                
    def write_gift_reactions_to_db(gift_reactions):
        conn = sqlite3.connect("SDV.db")
        c = conn.cursor()
        for gift_reaction in gift_reactions:
            villager = gift_reaction.villager
            item = gift_reaction.item
            reaction = gift_reaction.reaction
            c.execute("INSERT INTO gifts VALUES (?, ?, ?)",
                                       (villager, item, reaction))
        conn.commit()
        conn.close()
        

    
class GiftReaction:
    def __init__(self, villager, item, reaction):
        self.villager = villager
        self.item = item
        self.reaction = reaction

    
if __name__ == "__main__":
    base = "https://stardewvalleywiki.com/"
    path = "/Category:Items"

    item_links = get_item_links(urljoin(base, path))
    write_giftable_items(item_links)