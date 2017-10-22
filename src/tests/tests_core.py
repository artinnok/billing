from unittest.mock import patch

from django import forms
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from core.models import Transaction


class BaseTestCase(TestCase):
    fixtures = ['core.json']

    def setUp(self):
        self.maxDiff = None

        self.user_model = get_user_model()
        self.user = self.user_model.objects.get(pk=1)

        self.client = Client()

        self.patcher = patch('core.forms.Profile')
        self.mock = self.patcher.start()
        self.mock.objects.all.return_value.values_list.return_value = [('45192278', '1')]

    def tearDown(self):
        self.patcher.stop()


class TransactionTestCase(BaseTestCase):

    def test_some_users_not_found(self):
        try:
            response = self.client.post(
                reverse('index'),
                data={
                    'sender': '45192278',
                    'receiver_list': '1, 2',
                    'amount': 10.00,
                },
            )

        except (forms.ValidationError, KeyError):
            self.fail()

    def test_profile_not_found(self):
        try:
            response = self.client.post(
                reverse('index'),
                data={
                    'sender': '10',
                    'receiver_list': '45192278',
                    'amount': 10.00,
                },
            )

        except (forms.ValidationError, KeyError):
            self.fail()

    def test_not_enough_funds(self):
        try:
            response = self.client.post(
                reverse('index'),
                data={
                    'sender': '66904023',
                    'receiver_list': '45192278',
                    'amount': 10.00,
                },
            )

        except (forms.ValidationError, KeyError):
            self.fail()

    def test_success(self):
        old_transaction_count = Transaction.objects.count()

        response = self.client.post(
            '/',
            data={
                'sender': ['66904023'],
                'receiver_list': '66904023',
                'amount': 10.00,
            },
        )

        expected = {
            'success': True,
        }

        self.assertEqual(old_transaction_count + 1, Transaction.objects.count())
        self.assertEqual(expected, response.json())
