import json
import unittest

from app import init_server
from tests.base import AbstractTest


class CategoryAPITest(AbstractTest):
    tables = ['category']

    client = init_server().test_client()

    def setUp(self):
        super().setUp()

        self.load_fixtures()

    def test_get(self):
        response = self.client.get('/category')

        actual = json.loads(response.data.decode())
        expect = [
            {'category_id': 1, 'name': '雑談'},
            {'category_id': 2, 'name': '恋愛'},
            {'category_id': 3, 'name': '学業'},
        ]

        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
