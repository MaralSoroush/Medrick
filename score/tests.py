from django.test import TestCase
from .models import Score
from random import randint

# Create your tests here.


class ScoreBoardTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        record_number = 10
        for i in range(1, record_number + 1):
            Score.objects.create(player_id=i, score=randint(0, 100))

    def test_with_valid_player_id(self):
        response = self.client.get('/game/score?playerid=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), [
                         "player_id", "score", "rank", "records"])

    def test_with_non_existance_player_id(self):
        response = self.client.get('/game/score?playerid=50')
        self.assertEqual(response.status_code, 404)

    def test_with_invalid_player_id(self):
        response = self.client.get('/game/score?playerid=test')
        self.assertEqual(response.status_code, 400)

    def test_without_player_id(self):
        response = self.client.get('/game/score')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ["records"])


class CreateScoreTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        record_number = 10
        for i in range(1, record_number + 1):
            Score.objects.create(player_id=i, score=randint(0, 100))

    def test_with_valid_data(self):
        response = self.client.post(
            path='/game/score', data={'player_id': 11, 'score': 50})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(list(response.data.keys()), [
                         "player_id", "score", "datetime"])

    def test_with_repetitive_player_id(self):
        response = self.client.post(
            path='/game/score', data={'player_id': 5, 'score': 50})
        self.assertEqual(response.status_code, 400)

    def test_with_invalid_score(self):
        response = self.client.post(
            path='/game/score', data={'player_id': 15, 'score': -50})
        self.assertEqual(response.status_code, 400)
