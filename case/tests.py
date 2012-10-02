# Copyright (c) 2012 Jason McVetta.


from django.test import TestCase
from django.contrib.auth.models import User


class CaseViewsTestCase(TestCase):
    
    def setUp(self):
        User.objects.create_user('kirk', 'kirk-testuser@creditswarm.com', 'password')
    
    def test_index(self):
        "Test index page"
        c = self.client
        resp = c.get('/')
        self.assertEqual(resp.status_code, 200)
        resp = c.login(username='kirk', password='password')
        self.assertTrue(resp, 'Unable to login as test user "kirk"')

