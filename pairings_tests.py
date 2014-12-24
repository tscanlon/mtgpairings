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

    def add_event(self, data):
        return self.app.post('/add_event', data=data, follow_redirects=True)

    def add_round(self, data):
        return self.app.post('/event/1/', data=data, follow_redirects=True)

    def test_add_event(self):
        data=dict(
            event_name='Test',
            mtg_format='Legacy'
        )
        assert 'Test: Legacy' in self.add_event(data).data
    
    def test_view_event(self):
        data=dict(
            event_name='Test',
            mtg_format='Legacy'
        )
        self.add_event(data)
        rv = self.app.get('/event/1')
        assert 'Test: Legacy' in rv.data

    def test_add_round(self):
        event_data=dict(
            event_name='Test',
            mtg_format='Legacy'
        )
        round_data=dict(
            round_number = '1',
            event_id = '1',
            pairings = "Herp plays derp\n terp plays verp"
        )
        rv_event = self.add_round(event_data)
        rv_add_round = self.add_round(round_data)
        # test updating a round pairings
        round_data['pairings'] = "derp plays verp\n terp plays herp"
        rv_add_round = self.add_round(round_data)
        rv_view_round =  self.app.get('/event/1/1')
        assert 'Test: Legacy' in rv_event.data
        assert '<a href="/event/1/1"> 1</a>' in rv_add_round.data
        assert 'derp plays verp' in rv_view_round.data


if __name__ == '__main__':
    unittest.main()
