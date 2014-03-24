from django.test import TestCase


class ApiTest(TestCase):

    def login_user1(self):
        self.client.login(username='test', password='test')

    def login_user2(self):
        self.client.login(username='test2', password='test2')
