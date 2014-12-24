import os
import mtgpairings
import unittest
import tempfile

class PairingsTestCase(unittest.TestCase):
    def setUp(self):
        # setup a temp db
        self.db_fd, mtgpairings.app.config['DATABASE'] = tempfile.mkstemp()
        # set flask to testing
        mtgpairings.app.config['TESTING'] = True
        self.app = mtgpairings.app.test_client()
        mtgpairings.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(mtgpairings.app.config['DATABASE'])

    def test_event(self):
        rv = self.app.post('/add_event', data=dict(
            event_name='Test',
            mtg_format='Legacy'
        ), follow_redirects=True)
        assert 'Test: Legacy' in rv.data

if __name__ == '__main__':
    unittest.main()
