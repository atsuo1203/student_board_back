import unittest

from app.models.category import Category
from tests.base import AbstractTest


class CategoryTest(AbstractTest):
    tables = ['category']

    def setUp(self):
        super().setUp()

        self.load_fixtures()

    def test_get(self):
        category = Category()

        actual = category.get()
        expect = [
            {'category_id': 1, 'name': '雑談'},
            {'category_id': 2, 'name': '恋愛'},
            {'category_id': 3, 'name': '学業'},
        ]

        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
