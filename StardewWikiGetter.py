import requests
import bs4
import json
from SVWikiScraper import GiftReaction

class StardewWikiGetter:
    API_URL = "https://stardewvalleywiki.com/mediawiki/api.php"
    ITEM_PAGE_TITLE = "Category:Items"
    
    def __init__(self, category_page_title):
        self.category_page_title = category_page_title
        
    def get_giftable_item_reactions(self):
        item_pageids = self.get_item_pageids()
        return self.get_giftable_item_reactions_from_item_pageids(
            item_pageids)
        
    def get_giftable_item_reactions_from_item_pageids(self, pageids):
        gift_reactions = list()
        
        for pageid in pageids:
            print(pageid)
            page_parse = self.parse(pageid)
            if self.isItemGiftable(page_parse):
                gift_reactions.extend(
                    self.get_gift_reactions(page_parse))
                
        return gift_reactions
    
    def get_gift_reactions(self, item_page_parse):
        reactions = []
    
        html_content = item_page_parse["parse"]["text"]["*"]
        html = bs4.BeautifulSoup(html_content, "html.parser")

        item = html.find(id="infoboxheader").text.strip("\n ")
        gift_header = html.find(id="Gifting")
        if not gift_header:
            print("Not a gift")
            return reactions
        
        rows = gift_header.parent.find_next("table").find_all("tr")
        table_name = rows[0].text.strip("\n ")
        if table_name != "Villager Reactions":
            print("NO")
            return reactions
            

        for row in rows[1:]:
            reaction = row.find("th").text.strip("\n ")
            villagers = [x.text.strip("\n ") for x in row.find_all("div")]
            for villager in villagers:
                reactions.append(GiftReaction(villager, item, reaction))
        
        return reactions
        
        
    
    def isItemGiftable(self, item_page_parse):
        parse = item_page_parse["parse"]
        if "sections" not in parse:
            print("no sections")
            return False
        
        for section in parse["sections"]:
            if "line" in section and section["line"] == "Gifting":
                print("giftable")
                return True
        return False
        
    def get_item_pageids(self):
        """
            Return a set of all pageids for item pages in the
            category being queried.
        """
        print("opening: " + self.category_page_title)
        query = self.query(self.category_page_title)
        item_pageids = self.get_all_item_pageids_from_query(query)
        
        while "continue" in query:
            query = self.query(
                self.category_page_title, 
                query["continue"]["cmcontinue"])
            print("continuing: " + self.category_page_title)
            item_pageids.union(
                self.get_all_item_pageids_from_query(query))
            
        return item_pageids
        
    def get_all_item_pageids_from_query(self, query):
        """
            Returns a set of all pageids for item pages 
        """
        item_pageids = set()
        category_members = query["query"]["categorymembers"]
        for member in category_members:
            member_title = member["title"]
            if member_title.startswith("Category:"):
                subcat_querier = StardewWikiGetter(member_title)
                item_pageids.union(
                    subcat_querier.get_item_pageids())
            else:
                item_pageids.add(member["pageid"])
                print(f"{member['pageid']}: + {member_title}")
        
        return item_pageids
        
    def query(self, category, continueid = None):
        """
            Query the wiki for categorymembers of the given category 
            and return the result.
        """

        params = {
            "action": "query", 
            "list": "categorymembers", 
            "cmtitle": category, 
            "format": "json"}
        if continueid:
            params["cmcontinue"] = continueid
            
        response = requests.get(self.API_URL, params)
        return json.loads(response.text)
    
    def parse(self, pageid):
        params = {
            "action": "parse",
            "pageid": pageid,
            "format": "json"
        }
        
        response = requests.get(self.API_URL, params)
        return json.loads(response.text)