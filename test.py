from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_show_start(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<table id="boggle-table">', html)
            self.assertIn('<td>?</td>', html)
    
    def test_show_board(self):
        with app.test_client() as client:
            resp = client.get('/start')

            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(session['board'], list)
            self.assertIsInstance(session['board'][0][0], str)
    
    def test_submit_word(self):
        board = [['A', 'B', 'C', 'D', 'E'],
                 ['V', 'E', 'D', 'R', 'W'],
                 ['G', 'M', 'B', 'U', 'X'],
                 ['Q', 'O', 'V', 'V', 'E'],
                 ['G', 'R', 'A', 'Y', 'P']]
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = board
            headers = {
                'Content-type':'application/json', 
                'Accept':'application/json'
            }
            # Debugging statement: Print session before making the request
            #print("Session before request:", change_session)

            resp = client.post("/submit", 
                                json={"word": "grave"},
                                headers=headers)
                                # Debugging statement: Print session before making the request
            #print("Session after request:", change_session)

            html = resp.get_data(as_text=True)
            #print(resp.json)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json["result"], "ok")

    def test_endGame(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 2
                change_session['number_of_plays'] = 2
            headers = {
                'Content-type':'application/json', 
                'Accept':'application/json'
            }
            dom_element =   """
                            <h2 class="score-box" id="high-score">5</h2>
                            """
            resp = client.post("/endgame",
                                json={"score": 5},
                                headers=headers)
            json_string = resp.get_data(as_text=True)
            #just realized I could've used resp.json instead. Might change later

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['high_score'], 5)
            self.assertEqual(session['number_of_plays'], 3)
            self.assertIn('"high_score":5', json_string)
            self.assertIn('"number_of_plays":3', json_string)
    
    def test_restart(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 7

            resp = client.get("/restart", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(resp.history), 1) #Check that there was one redirect
            self.assertEqual(resp.request.path, "/start") #Check that redirect was to the '/start' page
            self.assertIn('<h1 id="boggle-title">Boggle</h1>', html)
            self.assertIn('<h2 class="score-box" id="high-score">7</h2>', html)
            
