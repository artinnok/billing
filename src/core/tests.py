from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class BaseTestCase(TestCase):
    fixtures = ['core.json']

    def setUp(self):
        self.maxDiff = None

        self.user_model = get_user_model()
        self.user = self.user_model.objects.get(pk=1)

        self.client = Client()
