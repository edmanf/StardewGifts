from unittest import TestCase
from StardewGifts.WikiItemParser import WikiItemParser
from StardewGifts.WikiGetter import WikiGetter


class Test(TestCase):
    def test_ignore_XP_attribute(self):
        """ Currently XP is not supported, so it should not appear
        as an attribute. """
        pageid = 2486  # Oak Resin

        getter = WikiGetter()
        parse = getter.parse(pageid)
        parser = WikiItemParser(parse)
        item = parser.get_item()
        self.assertFalse("XP" in item.attributes)

    def test_bullet_list(self):
        expected_sources = ["Tapper  6-7 days", " Haunted Skull (1.30%)"]

        pageid = 8585  # oak resin
        item = WikiGetter().get_items_from_pageids([pageid]).item_attributes
        sources = item[0].attributes["sources"]
        self.assertEqual(expected_sources[0], sources[0])
        self.assertEqual(expected_sources[1], sources[1])

    def test_parse(self):
        ids = [1921, 1961, 2106, 2486, 2716, 3711,
               5665, 8585, 2489, 3487]
        getter = WikiGetter()
        for id in ids:
            item = getter.get_items_from_pageids([id])
            self.assertTrue(item.item_attributes, "{} failed".format(id))
