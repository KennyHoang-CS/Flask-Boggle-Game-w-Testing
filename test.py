from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """ Is the information in session and HTML being displayed? """

        with self.client:
            response = self.client.get('/')
            self.assertIn('board',session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_plays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'<p>Score:', response.data)
            self.assertIn(b'<p>Seconds Remaining:', response.data)

    def test_valid_word(self):
        """ Is the word valid from board interactions? """

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ["D", "O", "G", "G", "G"],
                    ["D", "O", "G", "G", "G"],
                    ["D", "O", "G", "G", "G"],
                    ["D", "O", "G", "G", "G"],
                    ["D", "O", "G", "G", "G"],
                ]
                response = self.client.get('/check-word?word=dog')
                self.assertEqual(response.json['result'], 'ok')


    def test_invalid_word(self):
        """ Test if word is in dictionary. """

        self.client.get('/')
        response = self.client.get('/check-word?word=whyyyyyy')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """ Test if word is on the board. """

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=saijdsajikdsaj')
        self.assertEqual(response.json['result'], 'not-word')