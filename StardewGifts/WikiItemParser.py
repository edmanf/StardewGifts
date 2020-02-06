import bs4
import functools
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
            if section.text.startswith("Sell Price"):
                # Not currently supporting Sell Prices
                # I believe all Sell Prices are listed at the bottom,
                # So should not remove any other information
                break
                
            section_name = self.get_section_name(section)


            if section_name == "XP" or section_name == "Healing Effect":
                # ignore XP and healing effect for now
                continue
            if self.section_is_attribute(section):
                values = self.get_attribute_values(section)
                item.attributes[section_name] = values
                
        return item
        
    def get_attribute_values(self, section):
        """ Returns a list of attribute values from the given section. """
        details = section.parent.find(id = "infoboxdetail")
        spans = details.find_all("span")
        values = []
        if spans:
            for span in spans:
                values.append(span.text.strip())
            return values
            
        li_tags = details.find_all("li")
        if li_tags:
            for li in li_tags:
                values.append(li.text.strip())
            return values
            
        a_tags = details.find("a")
        if a_tags:
            for a_tag in a_tags:
                value = a_tag.string.strip()
                if value == "Seasons":
                    values.append("All Seasons")
                else:
                    values.append(value)
                
            return values

        return [section.parent.find(id = "infoboxdetail").text.strip()]
            
        
    def get_section_name(self, section):
        parts = section.text.split(":")
        # handles the case where an item has : in its name by
        # only removing the last :
        return "".join(parts[:-1])
        
    def section_is_attribute(self, section):
        return section.text.find(":") != -1
    