import unittest
import json
from backend.app import app

class TestBackend(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        response = self.app.get('/api/health')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
    
    def test_calculate_risk(self):
        test_data = {
            'amount': 5000,
            'age': 30,
            'category': 'grocery',
            'state': 'KA',
            'user_id': 'test@example.com'
        }
        response = self.app.post('/api/calculate-risk', 
                                 json=test_data,
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('risk', data)
    
    def test_set_balance(self):
        test_data = {
            'user_id': 'test@example.com',
            'balance': 25000
        }
        response = self.app.post('/api/set-balance',
                                 json=test_data,
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['balance'], 25000)
    
    def test_get_balance(self):
        response = self.app.get('/api/get-balance?user_id=test@example.com')
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_register_transaction(self):
        test_data = {
            'user_id': 'test@example.com',
            'to': 'test@okhdfcbank',
            'amount': 1000,
            'risk_score': 15,
            'risk_level': 'Low'
        }
        response = self.app.post('/api/register-transaction',
                                 json=test_data,
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()