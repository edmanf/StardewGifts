import requests
import json
from StardewGifts.GiftReaction import GiftReaction
from StardewGifts.StardewWikiItemParser import StardewWikiItemParser

class StardewWikiGetter:
    """ This class retrieves information from Stardew wiki webpages """

    API_URL = "https://stardewvalleywiki.com/mediawiki/api.php"
    ITEM_PAGE_TITLE = "Category:Items"
    
    limit = 10
    LIMIT_ON = False
    
    def __init__(self, category_page_title = self.ITEM_PAGE_TITLE):
        self.category_page_title = category_page_title
        
    def get_giftable_item_reactions(self):
        """
            Returns a list of GiftReactions with information taken from the
            wiki.
        """
        item_pageids = self.get_item_pageids()
        return self.get_giftable_item_reactions_from_item_pageids(
            item_pageids)
        
    def get_giftable_item_reactions_from_item_pageids(self, pageids):
        """
            Returns a list of GiftReactions from each 
        """
        gift_reactions = list()
        
        for pageid in pageids:
            parser = StardewWikiItemParser(self.parse(pageid))
            if parser.isItemGiftable():
                gift_reactions.extend(
                    parser.get_gift_reactions())
                print(f"added gift: {pageid}")
                
        return Result(gift_reactions = gift_reactions)
        
    def get_items(self):
        item_pageids = self.get_item_pageids()
        return self.get_items_from_pageids(self, item_pageids)
        
    def get_items_from_pageids(self, pageids):
        items = list()
        
        for pageid in pageids:
            parser = StardewWikiItemParser(self.parse(pageid))
            items.extend(parser.get_item())
                
        return Result(items = items)
        
    def get_items_and_gift_reactions(self):
        item_pageids = self.get_item_pageids()
        return self.get_items_and_gift_reactions_from_pageids
        
    def get_items_and_gift_reactions_from_pageids(self, pageids):
        # don't use existing get_items_from_pageids() or 
        # get_giftable_item_reactions_from_item_pageids()
        # to avoid calling the API twice per pageid
        
        items = list()
        gift_reactions = list()
        
        for pageid in pageids:
            parser = StardewWikiItemParser(self.parse(pageid))
            items.extend(parser.get_item())
            if parser.isItemGiftable():
                gift_reactions.extend(
                    parser.get_gift_reactions())
        return Result(items = items, gift_reactions = gift_reactions)

    def get_item_pageids(self):
        """
            Return a set of all pageids for item pages in the
            category being queried.
        """
        print(f"checking {self.category_page_title}")
        query = self.query(self.category_page_title)
        item_pageids = self.get_all_item_pageids_from_query(query)
        
        while "continue" in query:
            query = self.query(
                self.category_page_title, 
                query["continue"]["cmcontinue"])
            new_ids = self.get_all_item_pageids_from_query(query)
            item_pageids = item_pageids.union(new_ids)

        return item_pageids
        
    def get_all_item_pageids_from_query(self, query):
        """
            Returns a set of all pageids for item pages 
        """
        
        if self.limit <= 0 and self.LIMIT_ON:
            return set()
        
        item_pageids = set()
        category_members = query["query"]["categorymembers"]
        for member in category_members:
            member_title = member["title"]
            if member_title.startswith("Category:"):
                subcat_querier = StardewWikiGetter(member_title)
                item_pageids = item_pageids.union(
                    subcat_querier.get_item_pageids())
            else:
                item_pageids.add(member["pageid"])
                print(f"getting item {member['pageid']}:{member_title}")
                self.limit -= 1
        
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
        
    class Result:
        def __init__(self, items = None, gift_reactions = None):
            self.items = items
            self.gift_reactions = gift_reactions