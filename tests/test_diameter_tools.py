from unittest import TestCase

from eco.diameter_tools import get_area, get_trunk_diam


class TestArea(TestCase):
    def test_area(self):
        circumference = 50.0
        area = get_area(circumference)

        self.assertEqual(area, 198.94367886486916)

    def test_diam1(self):
        r = get_trunk_diam('10, 10')

        self.assertEqual(r, 4.501581580785531)

    def test_diam2(self):
        r = get_trunk_diam('10, 10, 10')

        self.assertEqual(r, 5.513288954217921)

    def test_diam3(self):
        r = get_trunk_diam('10,')

        self.assertEqual(r, 3.183098861837907)

    def test_diam4(self):
        r = get_trunk_diam('17, 9, 8, 10, 11')

        self.assertEqual(r, 8.146494662474852)
