import unittest
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app import app

class TestJenkinsPipelineApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_returns_200(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_home_has_message(self):
        r = self.client.get('/')
        data = json.loads(r.data)
        self.assertIn('message', data)

    def test_health_returns_healthy(self):
        r = self.client.get('/health')
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data)
        self.assertEqual(data['status'], 'healthy')

if __name__ == '__main__':
    unittest.main(verbosity=2)
