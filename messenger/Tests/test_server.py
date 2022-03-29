import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.settings import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import Server


class TestServer(unittest.TestCase):
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}

    def setUp(self):
        self.server = Server()

    def test_ok_check(self):
        self.assertEqual(self.server.process({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.ok_dict)

    def test_no_action(self):
        self.assertEqual(self.server.process({TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(self.server.process({ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.err_dict)

    def test_no_time(self):
        self.assertEqual(self.server.process({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(self.server.process({ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        self.assertEqual(self.server.process({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest_1'}}),
                         self.err_dict)


if __name__ == '__main__':
    unittest.main()
