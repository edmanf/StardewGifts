from StardewGifts import WikiApiHelper
from StardewGifts.WikiItemParser import WikiItemParser


class WikiGetter:
    """ This class retrieves information from Stardew wiki webpages """

    CATEGORY_PAGE_TITLES = frozenset(["Category:Items", "Category:Foraging"])

    limit = 10
    LIMIT_ON = False

    def __init__(self, category_page_titles=CATEGORY_PAGE_TITLES):
        self.category_page_titles = category_page_titles

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
            parser = WikiItemParser(WikiApiHelper.action_parse_pageid(pageid))
            if parser.is_item_giftable():
                gift_reactions.extend(
                    parser.get_gift_reactions())
                print(f"added gift: {pageid}")

        return WikiGetter.Result(gift_reactions=gift_reactions)

    def get_items(self):
        item_pageids = self.get_item_pageids()
        return self.get_items_from_pageids(item_pageids)

    def get_items_from_pageids(self, pageids):
        items = list()

        for pageid in pageids:
            parser = WikiItemParser(WikiApiHelper.action_parse_pageid(pageid))
            if parser.is_item_giftable():
                items.append(parser.get_item())

        return WikiGetter.Result(items=items)

    def get_items_and_gift_reactions(self):
        item_pageids = self.get_item_pageids()
        return self.get_items_and_gift_reactions_from_pageids(item_pageids)

    def get_items_and_gift_reactions_from_pageids(self, pageids):
        # don't use existing get_items_from_pageids() or 
        # get_giftable_item_reactions_from_item_pageids()
        # to avoid calling the API twice per pageid

        items = list()
        gift_reactions = list()

        for pageid in pageids:
            parser = WikiItemParser(WikiApiHelper.action_parse_pageid(pageid))
            if parser.is_item_giftable():
                items.append(parser.get_item())
                gift_reactions.extend(
                    parser.get_gift_reactions())
        return WikiGetter.Result(items=items, gift_reactions=gift_reactions)

    def get_item_pageids(self):
        """
            Return a set of all pageids for item pages in the
            category being queried.
        """
        item_pageids = set()
        for category in self.category_page_titles:
            print(f"checking {category}")
            query = WikiApiHelper.action_query_category(category)
            item_pageids = item_pageids.union(self.get_all_item_pageids_from_query(query))

            while "continue" in query:
                query = WikiApiHelper.action_query_category(
                    category,
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
                subcat_querier = WikiGetter(category_page_titles=frozenset([member_title]))
                item_pageids = item_pageids.union(
                    subcat_querier.get_item_pageids())
            else:
                item_pageids.add(member["pageid"])
                print(f"getting item {member['pageid']}:{member_title}")
                self.limit -= 1

        return item_pageids

    class Result:
        def __init__(self, items=None, gift_reactions=None):
            self.items = items
            self.gift_reactions = gift_reactions
