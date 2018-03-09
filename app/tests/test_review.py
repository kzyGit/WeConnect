import unittest
import os
import json
from app import create_app
from app.models import Review
from app.models import Business
 
class TestReviewClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.reviews = {'title':'my business', 'content':'about location'}

    def test_create_business_review(self):        
        # self.client.post('/api/v1/businesses', data=self.business)        
        response = self.client.post('/api/businesses/1/review', data=self.reviews)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Review added successfully", response_msg["message"])


    def tearDown(self):
        Review.reviews=[]