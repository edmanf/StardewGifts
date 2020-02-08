import bs4
import functools
from StardewGifts.GiftReaction import GiftReaction
from StardewGifts.Item import Item


class WikiItemParser:
    """ This class extracts relevant item and gift information from 
    the results of action=parse in the stardew wiki API """
    def __init__(self, parse):
        self.parse = parse
        print(parse["parse"]["pageid"])
        
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
                # Special case
                # Sell price is unsupported because sometimes its
                # detail is another table, with more sections.
                # Currently believe all sell prices are listed at the
                # end, so it is safe to just break
                break
                
            section_name = self.get_section_name(section)


            if self.section_is_supported_attribute(section):
                values = self.get_attribute_values(section)
                item.attributes[section_name] = values
                
        return item
        
    def get_attribute_values(self, section):
        """ Returns a list of attribute values from the given section. """
        
        
        """
            Corner cases:
                Dinosaur egg source
                    (<a text>) seperator (<a text>) seperator (<a text>)
                oak resin source
                    (<li <a text> <span <img> text>>)
                    (<li <span <img> <a text>>>)
                tuna season
                    (<span <a <img>> <a text>>) separator (<span <a <img>> <a text>>)
                quartz season
                    (<span <img> <a text>>) (<span <img> <a text> text>) (<span <img> <a text> text>)
                maple syrup source
                    <a text> <span <img> text>
        
        """
        details = section.parent.find(id = "infoboxdetail")
        values = []
        
        li_tags = details.find_all("li")
        if li_tags:
            for li in li_tags:
                values.append(li.text.strip())
            return values
        
        spans = details.find_all("span")
        if spans:
            for span in spans:
                if span.previous.string == "Tapper":
                    # handles the tapper (maple syrup, pine tar) corner case
                    values.append(span.parent.text.strip())
                else:
                    values.append(span.text.strip())
            return values
            
        
            
        a_tags = details.find_all("a")
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
        """ Gets the section name from an infoboxsection. """
        
        # handles the case where an item has : in its name by
        # only removing the last :
        parts = section.text.split(":")
        return "".join(parts[:-1])
        
    def section_is_supported_attribute(self, section):
        """ Returns true if the section is a supported attribute. """
        
        if (section.text.startswith("XP") or 
            section.text.startswith("Healing Effect")):
            return False
            
        return section.text.find(":") != -1
    