from unittest import TestCase

from eco.utils import session_scope


class TestSessionManager(TestCase):

    def setUp(self):
        with session_scope('sqlite:///:memory:') as manager:
            self.session = manager

    def test_session_resource(self):
        self.assertEqual({}, self.session.info)

    def test_session_catch_exception(self):
        with session_scope('sqlite:///') as manager:
            session = manager
            with self.assertRaises(AttributeError):
                session.should_fail()
