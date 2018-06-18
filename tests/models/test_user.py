import unittest

from app.models.user import User
from tests.base import AbstractTest


class UserTest(AbstractTest):
    tables = ['user']
    test_tables = ['user']

    def test_get(self):
        '''user_idに紐づく必要最低限のuser情報の取得
        '''
        self.load_fixtures()

        user = User()

        actual = user.get(1)
        expect = {
            'nick_name': None,
            'profile': None,
            'twitter_name': None,
        }

        self.assertDictEqual(expect, actual)

        actual = user.get(2)
        expect = {
            'nick_name': 'sakura',
            'profile': 'profile_sakura',
            'twitter_name': 'tw_sakura',
        }

        self.assertDictEqual(expect, actual)

    def test_get_no_user(self):
        '''存在しないuser_idを指定した場合
        '''
        self.load_fixtures()

        user = User()

        actual = user.get(100)

        self.assertEqual(None, actual)

    def test_get_user_all(self):
        '''user_idに紐づくuser情報の取得
        '''
        self.load_fixtures()

        actual = User.get_user_all(1)
        expect = {
            'user_id': 1,
            'email': 'test1@test_gmail.com',
            'nick_name': None,
            'profile': None,
            'twitter_name': None,
        }

        self.assertDictEqual(expect, actual)

    def test_get_users_all(self):
        '''すべてのuser情報取得
        '''
        self.load_fixtures()

        actual = User.get_users_all()
        expect = [
            {
                'user_id': 1,
                'email': 'test1@test_gmail.com',
                'nick_name': None,
                'profile': None,
                'twitter_name': None,
            },
            {
                'user_id': 2,
                'email': 'test2@test_gmail.com',
                'nick_name': 'sakura',
                'profile': 'profile_sakura',
                'twitter_name': 'tw_sakura',
            },
            {
                'user_id': 3,
                'email': 'test3@test_gmail.com',
                'nick_name': 'matsu',
                'profile': 'profile_matsu',
                'twitter_name': 'tw_matsu',
            },
        ]

        self.assertListEqual(expect, actual)

    def test_get_user_secret(self):
        '''user_idに紐づくuser情報(すべて)取得
        '''
        self.load_fixtures()

        user = self.filter_test_data(
            table='user', field='user_id', target=1
        )[0]

        actual = User.get_user_secret(1)
        expect = user

        self.assertDictEqual(expect, actual)

    def test_login(self):
        '''emailとpasswordからuser情報取得
        '''
        self.load_fixtures()

        user = User()

        actual = user.login(
            'test1@test_gmail.com',
            'test_pass1'
        )
        expect = {
            'user_id': 1,
            'email': 'test1@test_gmail.com',
            'nick_name': None,
            'profile': None,
            'twitter_name': None,
        }

        self.assertDictEqual(expect, actual)

    def test_login_no_user(self):
        '''emailとpasswordに一致するuserが存在しない場合
        '''
        self.load_fixtures()

        user = User()

        actual = user.login(
            'test100@test_gmail.com',
            'test_pass100'
        )

        self.assertEqual(None, actual)

    def test_is_exist(self):
        '''すでにuserが登録されている場合
        '''
        self.load_fixtures()

        user = User()

        actual = user.is_exist('test1@test_gmail.com')

        self.assertEqual(True, actual)

    def test_is_exist_no_user(self):
        '''userが登録されていない場合
        '''
        self.load_fixtures()

        user = User()

        # input(">3")
        actual = user.is_exist('test100@test_gmail.com')
        # input(">4")

        self.assertEqual(False, actual)

    def test_post(self):
        '''user登録
        登録されたuserのuser_idとemailが返却
        '''
        self.load_fixtures()

        user = User()

        actual = user.post('test4@test_gmail.com', 'test_pass4')
        expect = {
            'user_id': 4,
            'email': 'test4@test_gmail.com',
        }

        self.assertDictEqual(expect, actual)

    def test_put(self):
        '''user更新
        '''
        self.load_fixtures()

        data = {
            'nick_name': 'kiku',
        }

        User.put(1, data)
        actual = User.get(1)
        expect = {
            'nick_name': 'kiku',
            'profile': None,
            'twitter_name': None,
        }

        self.assertDictEqual(expect, actual)

    def test_put_password(self):
        '''userのpassword更新
        '''
        self.load_fixtures()

        new_password = 'new_pass'

        user = self.filter_test_data(
            table='user', field='user_id', target=1
        )[0]

        password = user.get('password')

        User.put_password(1, password, new_password)

        actual = User.get_user_secret(1)

        expect = user
        expect.update({
            'password': new_password
        })

        self.assertDictEqual(expect, actual)

    def test_put_password_invalid(self):
        '''userのpassword更新 間違ったpassword
        '''
        self.load_fixtures()

        new_password = 'new_pass'

        password = 'invalid_password'

        with self.assertRaises(Exception) as e:
            User.put_password(1, password, new_password)

        self.assertEqual(
            'invalid password',
            str(e.exception)
        )


if __name__ == '__main__':
    unittest.main()
