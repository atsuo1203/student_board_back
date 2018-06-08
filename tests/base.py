import unittest
from sqlalchemy import create_engine

from app.config import create_dburl, current_config
from tests.utils import (
    create_database,
    drop_database,
    create_tables
)


class AbstractTest(unittest.TestCase):
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
