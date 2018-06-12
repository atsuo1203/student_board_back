import yaml

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_seed import load_fixture_files as ss_load_fixture_files
from sqlalchemy_seed import load_fixtures as ss_load_fixtures
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database as _drop_database

from app.config import create_dburl, current_config
from app.models import session_scope


models_path = 'app.models'


def create_database():
    '''データベース作成
    '''
    # データベース名取得
    db = current_config('db')

    dburl = create_dburl()
    dburl = dburl[:dburl.rfind('/')]

    engine = create_engine(dburl)
    conn = engine.connect()
    conn.execute(
        'CREATE DATABASE %s CHARACTER SET %s;'
        % (db.get('db'), db.get('charset'))
    )
    conn.close()


def drop_database():
    '''データベース削除
        envのDBを対象とする
    '''
    dburl = create_dburl()

    if database_exists(dburl):
        _drop_database(dburl)


def create_tables():
    '''全テーブル作成（commentテーブル以外を作成）
    '''
    db_modules = __import__(models_path, fromlist=[''])

    with session_scope() as session:
        Base = getattr(db_modules, 'Base')
        Base.metadata.create_all(bind=session.bind)


def drop_tables():
    '''全テーブル初期化
    '''
    db_modules = __import__(models_path, fromlist=[''])

    with session_scope() as session:
        Base = getattr(db_modules, 'Base')
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())


def load_fixtures(fixtures_root, tables):
    '''テストデータ読み込み
    '''
    if not tables:
        return

    fixtures_data_path = ['%s.yaml' % table for table in tables]

    for table in fixtures_data_path:
        # fixtures_dataを読み込み
        fixture_data = ss_load_fixture_files(fixtures_root, [table])

        with session_scope() as session:
            # fixtures_dataをテーブルに格納
            ss_load_fixtures(session, fixture_data)


def load_comment_fixtures(fixtures_root, tables):
    '''commentテストデータ読み込み
    '''
    root_path = __file__[:__file__.rfind('tests')]

    for table_name in tables:
        path = '%s/%s/%s.yaml' % (root_path, fixtures_root, table_name)

        with open(path, 'r') as f:
            data_list = yaml.load(f)

            with session_scope() as session:
                for data in data_list:
                    dburl = create_dburl()
                    engine = create_engine(dburl)
                    base = declarative_base(engine)

                    comment_table_dic = {
                        '__tablename__': table_name,
                        '__table_args__': {'autoload': True}
                    }
                    comment_table = type(
                        'comment_table', (base,), comment_table_dic
                    )

                    data = comment_table(
                        **data
                    )
                    session.add(data)
