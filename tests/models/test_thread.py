import datetime
import unittest

from freezegun import freeze_time

from app.models.thread import Thread
from tests.base import AbstractTest


class ThreadTest(AbstractTest):
    tables = ['user', 'category', 'thread']
    comment_tables = ['comment1', 'comment2']

    def tearDown(self):
        # 先にcommentテーブルを削除
        self.drop_comment_tables()

        super(ThreadTest, self).tearDown()

    def test_get_all(self):
        '''すべてのthread情報取得
        '''
        self.load_fixtures()

        self.create_comment_tables()
        self.load_comment_fixtures()

        thread = Thread()

        actual = thread.get_all()
        expect = [
            {
                'thread_id': 1,
                'title': 'title1',
                'create_at': datetime.datetime(2018, 1, 1, 0, 0),
                'update_at': datetime.datetime(2018, 1, 1, 0, 0),
                'speed': 0,
                'comment_count': 0,
                'category_id': 1,
            },
            {
                'thread_id': 2,
                'title': 'title2',
                'create_at': datetime.datetime(2018, 1, 2, 0, 0),
                'update_at': datetime.datetime(2018, 1, 2, 0, 0),
                'speed': 0,
                'comment_count': 0,
                'category_id': 1,
            },
            {
                'thread_id': 3,
                'title': 'title3',
                'create_at': datetime.datetime(2018, 1, 3, 0, 0),
                'update_at': datetime.datetime(2018, 1, 3, 0, 0),
                'speed': 120,
                'comment_count': 3,
                'category_id': 2,
            },
        ]

        self.assertListEqual(expect, actual)

    def test_get_all_by_category_id(self):
        '''category_idに紐づくthread情報のリスト取得
        '''
        self.load_fixtures()

        self.create_comment_tables()
        self.load_comment_fixtures()

        thread = Thread()

        actual = thread.get_all_by_category_id(1)
        expect = [
            {
                'thread_id': 1,
                'title': 'title1',
                'create_at': datetime.datetime(2018, 1, 1, 0, 0),
                'update_at': datetime.datetime(2018, 1, 1, 0, 0),
                'speed': 0,
                'comment_count': 0,
                'category_id': 1,
            },
            {
                'thread_id': 2,
                'title': 'title2',
                'create_at': datetime.datetime(2018, 1, 2, 0, 0),
                'update_at': datetime.datetime(2018, 1, 2, 0, 0),
                'speed': 0,
                'comment_count': 0,
                'category_id': 1,
            },
        ]

        self.assertListEqual(expect, actual)

    def test_get(self):
        '''thread_idに紐づくthread情報の取得
        '''
        self.load_fixtures()

        self.create_comment_tables()
        self.load_comment_fixtures()

        thread = Thread()

        actual = thread.get(1)
        expect = {
            'thread': {
                'thread_id': 1,
                'title': 'title1',
                'create_at': datetime.datetime(2018, 1, 1, 0, 0),
                'update_at': datetime.datetime(2018, 1, 1, 0, 0),
                'speed': 0,
                'comment_count': 0,
                'category_id': 1,
            },
            'comments': [
                {
                    'comment_id': 1,
                    'name': 'test_comment_1_1',
                    'text': 'test_text_1_1',
                    'create_at': datetime.datetime(2018, 1, 1, 0, 0),
                    'thread_id': 1,
                    'user_id': 1,
                },
                {
                    'comment_id': 2,
                    'name': 'test_comment_1_2',
                    'text': 'test_text_1_2',
                    'create_at': datetime.datetime(2018, 1, 1, 0, 0, 10),
                    'thread_id': 1,
                    'user_id': 1,
                },
            ]
        }

        self.assertDictEqual(expect, actual)

    @freeze_time('2018-01-03 00:00:00')
    def test_post(self):
        self.load_fixtures()

        self.create_comment_tables()
        self.load_comment_fixtures()

        thread = Thread()

        data = {
            'title': 'title4',
            'category_id': 1,
            'create_at': datetime.datetime.now(),
            'update_at': datetime.datetime.now(),
        }

        actual = thread.post(data)
        expect = {
            'thread_id': 4,
            'title': 'title4',
            'create_at': datetime.datetime(2018, 1, 3, 0, 0),
            'update_at': datetime.datetime(2018, 1, 3, 0, 0),
            'speed': 0,
            'comment_count': 0,
            'category_id': 1,
        }

        self.assertDictEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
