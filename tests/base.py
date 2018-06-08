import unittest
from sqlalchemy import create_engine

from app.config import create_dburl, current_config
from tests.utils import (
    create_database,
    create_tables,
    drop_database,
    load_fixtures,
)


fixture_data_root = 'tests/resources/data'


class AbstractTest(unittest.TestCase):
    # 利用するテーブル
    # 外部キー制約による読み込み順番に注意
    tables = []

    @classmethod
    def setUpClass(cls):
        # データベースの作成
        cls.create_database()

        # テーブルの作成
        cls.create_tables()

    @classmethod
    def tearDownClass(cls):
        # データベースの削除
        cls.drop_database()

    @classmethod
    def create_database(cls):
        '''テスト用データベース作成
        '''
        create_database()

    @classmethod
    def drop_database(cls):
        '''テスト用データベース削除
        '''
        drop_database()

    @classmethod
    def create_tables(cls):
        create_tables()

    @classmethod
    def load_fixtures(cls):
        '''テストデータを読み込む
        '''
        load_fixtures(fixture_data_root, cls.tables)
