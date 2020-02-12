from unittest import TestCase
from StardewGifts.WikiItemParser import WikiItemParser
from StardewGifts.WikiGetter import WikiGetter
from StardewGifts import WikiApiHelper


class Test(TestCase):
    def test_ignore_XP_attribute(self):
        """ Currently XP is not supported, so it should not appear
        as an attribute. """
        pageid = 2486  # Oak Resin

        getter = WikiGetter()
        parse = WikiApiHelper.action_parse_pageid(pageid)
        parser = WikiItemParser(parse)
        item = parser.get_item()
        self.assertFalse("XP" in item.attributes)

    def test_bullet_list(self):
        expected_sources = ["Tapper  6-7 days", "Haunted Skull\xa0(1.30%)"]

        pageid = 2105  # oak resin
        item = WikiGetter().get_items_from_pageids([pageid]).items
        sources = item[0].attributes["Source"]
        self.assertEqual(expected_sources[0], sources[0])
        self.assertEqual(expected_sources[1], sources[1])

    def test_parse(self):
        ids = [1921, 1961, 2106, 2486, 2716, 3711, 2105, 2489, 3487]
        getter = WikiGetter()
        for id in ids:
            result = getter.get_items_from_pageids([id])
            print(result.items)
            self.assertTrue(result.items, "{} failed".format(id))

    def test_get_non_giftable(self):
        pageid = 5665

        result = WikiGetter().get_items_from_pageids([pageid])
        items = result.items
        self.assertFalse(items)

        item = WikiItemParser(WikiApiHelper.action_parse_pageid(pageid)).get_item()
        self.assertTrue(item.attributes)

    def test_get_oak_resin(self):
        pageid = 2105
        result = WikiGetter().get_items_from_pageids([pageid])
        items = result.items
        self.assertTrue(items)
        item = items[0]

        expected_sources = ["Tapper  6-7 days", "Haunted Skull\xa0(1.30%)"]
        expected_seasons = ["Any Season"]

        self.assertEqual(len(items), 1)
        self.assertEqual(len(item.attributes), 2)
        self.assertEqual(item.attributes["Source"], expected_sources)
        self.assertEqual(item.attributes["Season"], expected_seasons)