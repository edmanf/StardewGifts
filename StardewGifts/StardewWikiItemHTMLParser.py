import bs4
from StardewGifts.GiftReaction import GiftReaction
from StardewGifts.StardewItem import StardewItem


class StardewWikiItemHTMLParser:
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
        item = StardewItem()
        item.name = parse.find(id="infoboxheader").text.strip()
        
        
        sections = parse.find_all(id = "infoboxsection")
        for section in sections:
            if section.text.startswith("Source:"):
                item.source = section.parent.find(id="infoboxdetail").text.strip()
            elif section.text.startswith("Season:"):
                item.season = section.parent.find(id="infoboxdetail").text.strip()
                
        return item