import bs4
from StardewGifts.GiftReaction import GiftReaction
from StardewGifts.Item import Item


class WikiItemParser:
    """ This class extracts relevant item and gift information from 
    the results of action=parse in the stardew wiki API """
    def __init__(self, parse):
        self.parse = parse
        
    def isItemGiftable(self):
        parse = self.parse["parse"]
        if "sections" not in parse:
            return False
        
        for section in parse["sections"]:
            if "line" in section and section["line"] == "Gifting":
                return True
        return False
        
    
        
    def get_gift_reactions(self):
        reactions = []
        
        item = self.parse["parse"]["title"]
    
        html_content = self.parse["parse"]["text"]["*"]
        html = bs4.BeautifulSoup(html_content, "html.parser")
        
        gift_header = html.find(id="Gifting")
        if not gift_header:
            return reactions
        
        rows = gift_header.parent.find_next("table").find_all("tr")
        table_name = rows[0].text.strip("\n ")
        if table_name != "Villager Reactions":
            return reactions
            
        for row in rows[1:]:
            reaction = row.find("th").text.strip("\n ")
            villagers = [x.text.strip("\n ") for x in row.find_all("div")]
            for villager in villagers:
                reactions.append(GiftReaction(villager, item, reaction))
        
        return reactions
        
    def get_item(self):
        parse = self.parse["parse"]["text"]["*"]
        html = bs4.BeautifulSoup(parse, features="html.parser")
        item = Item()
        item.name = html.find(id="infoboxheader").text.strip()
        
        
        sections = html.find_all(id = "infoboxsection")
        for section in sections:
            if section.text.startswith("Source:"):
                sources = []
                links = section.parent.find(id="infoboxdetail").find_all("span")
                for link in links:
                    sources.append(link.text.strip())
                item.sources = sources
            elif section.text.startswith("Season:"):
                links = section.parent.find(id="infoboxdetail").find_all("span")
                seasons = []
                for link in links:
                    seasons.append(link.text.strip())
                item.seasons = seasons
                
        return item