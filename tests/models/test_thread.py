import datetime
import unittest

from freezegun import freeze_time

from app.config import current_config
from app.models.thread import Thread
from tests.base import AbstractTest


ID_ASC = current_config().get('ID_ASC')
ID_DESC = current_config().get('ID_DESC')
SPEED_ASC = current_config().get('SPEED_ASC')
SPEED_DESC = current_config().get('SPEED_DESC')
NUM_COMMENT_ASC = current_config().get('NUM_COMMENT_ASC')
NUM_COMMENT_DESC = current_config().get('NUM_COMMENT_DESC')


class ThreadTest(AbstractTest):
    tables = ['user', 'category', 'thread', 'comment']
    test_tables = ['thread', 'comment']

    # @classmethod
    # def setUpClass(cls):
    #     super(ThreadTest, cls).setUpClass()

    #     cls.get_fixtures('thread')

    def test_get_all(self):
        '''すべてのthread取得
        '''
        self.load_fixtures()

        thread = Thread()

        actual = thread.get_all()
        expect = self.test_data.get('thread')

        self.assertListEqual(expect, actual)

    def test_get_sort_id_asc(self):
        '''ID昇順
        '''
        self.load_fixtures()

        thread = Thread()

        # ID昇順
        test_data = self.filter_test_data(
            table='thread', field='category_id', target=1, paging=1
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=ID_ASC, paging=1)

        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_sort_id_desc(self):
        '''ID降順
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread',
            field='category_id',
            target=1,
            paging=1,
            reverse=True
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=ID_DESC, paging=1
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_sort_speed_desc_1(self):
        '''人気高い順1
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread',
            field='thread_id',
            target=[6, 5, 1, 2, 7, 8, 9, 10, 11, 12]
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=SPEED_DESC, paging=1
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_sort_speed_desc_2(self):
        '''人気高い順2
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread', field='thread_id', target=[4, 3]
        )

        actual = thread.get_all_by_c_id(
            category_id=2, sort_id=SPEED_DESC, paging=1
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_sort_speed_asc(self):
        '''人気低い順
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread',
            field='thread_id',
            target=[1, 2, 23, 14, 7, 8, 9, 10, 11, 12]
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=SPEED_ASC, paging=1
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_sort_num_comment_desc(self):
        '''コメント数多い順
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread',
            field='thread_id',
            target=[6, 5, 1, 2, 7, 8, 9, 10, 11, 12]
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=SPEED_DESC, paging=1
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_sort_num_comment_asc(self):
        '''コメント数少ない順
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread',
            field='thread_id',
            target=[1, 2, 23, 14, 7, 8, 9, 10, 11, 12]
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=SPEED_ASC, paging=1
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_paging_1(self):
        '''ページング1-10
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread',
            field='thread_id',
            target=[1, 2, 5, 6, 7, 8, 9, 10, 11, 12]
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=ID_ASC, paging=1
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_paging_2(self):
        '''ページング11-20
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread',
            field='thread_id',
            target=[13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=ID_ASC, paging=2
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get_paging_3(self):
        '''ページング21-30
        '''
        self.load_fixtures()

        thread = Thread()

        test_data = self.filter_test_data(
            table='thread', field='thread_id', target=[23]
        )

        actual = thread.get_all_by_c_id(
            category_id=1, sort_id=ID_ASC, paging=3
        )
        expect = test_data

        self.assertListEqual(expect, actual)

    def test_get(self):
        '''thread_idに紐づくthread取得
        '''
        self.load_fixtures()

        thread = Thread()

        actual = thread.get(1)
        expect = {
            'thread': self.filter_test_data(
                table='thread', field='thread_id', target=[1]
            )[0],
            'comments': self.filter_test_data(
                table='comment', field='thread_id', target=[1]
            )
        }

        self.assertDictEqual(expect, actual)

    @freeze_time('2018-01-24 00:00:00')
    def test_post(self):
        '''新しいthread作成
        '''
        self.load_fixtures()

        thread = Thread()

        data = {
            'title': 'title24',
            'category_id': 1,
            'create_at': datetime.datetime.now(),
            'update_at': datetime.datetime.now(),
        }

        actual = thread.post(data)
        expect = {
            'thread_id': 24,
            'title': 'title24',
            'create_at': datetime.datetime(2018, 1, 24, 0, 0),
            'update_at': datetime.datetime(2018, 1, 24, 0, 0),
            'speed': 0,
            'comment_count': 0,
            'category_id': 1,
        }

        self.assertDictEqual(expect, actual)

    def test_delete(self):
        '''thread削除
        '''
        self.load_fixtures()

        thread = Thread()

        thread.delete(1)

        actual = thread.get(1)

        self.assertEqual(None, actual)

    def test_delete_no_thread(self):
        '''存在しないthread削除
        '''
        self.load_fixtures()

        thread = Thread()

        thread.delete(100)

        actual = thread.get(100)

        self.assertEqual(None, actual)


if __name__ == '__main__':
    unittest.main()
