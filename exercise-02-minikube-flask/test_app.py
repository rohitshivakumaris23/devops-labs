import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        """Set up test client."""
        app.testing = True
        self.client = app.test_client()

    def test_home_endpoint_status_code(self):
        """Test that home endpoint returns 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_endpoint_json_response(self):
        """Test that home endpoint returns valid JSON with expected fields."""
        response = self.client.get('/')
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertIn("version", data)
        self.assertEqual(data["version"], "1.0.0")

    def test_health_endpoint_status_code(self):
        """Test that health endpoint returns 200."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint_status_field(self):
        """Test that health endpoint returns healthy status."""
        response = self.client.get('/health')
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")

    def test_health_endpoint_service_name(self):
        """Test that health endpoint includes service name."""
        response = self.client.get('/health')
        data = json.loads(response.data)
        self.assertIn("service", data)

    def test_unknown_route_returns_404(self):
        """Test that unknown routes return 404."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main(verbosity=2)
