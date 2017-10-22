from unittest.mock import patch

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from core.models import Transaction


class BaseTestCase(TestCase):
    fixtures = ['core.json']

    def setUp(self):
        self.maxDiff = None

        self.user_model = get_user_model()
        self.user = self.user_model.objects.get(pk=1)

        self.client = Client()


class TransactionTestCase(BaseTestCase):

    def test_some_users_not_found(self):
        response = self.client.post(
            reverse('index'),
            data={
                'sender': '12',
                'receiver_list': '1, 2',
                'amount': 10.00,
            },
        )

        expected = {
            'errors': {
                'receiver_list': [
                    "Users with this INN ['1', '2'] not found"
                ]
            }
        }

        self.assertEqual(expected, response.json())

    def test_profile_not_found(self):
        response = self.client.post(
            reverse('index'),
            data={
                'sender': '100',
                'receiver_list': '45192278',
                'amount': 10.00,
            },
        )

        expected = {
            'errors': {
                'sender': [
                    'Select a valid choice. 100 is not one of the available choices.'
                ]
            }
        }

        self.assertEqual(expected, response.json())

    def test_not_enough_funds(self):
        response = self.client.post(
            reverse('index'),
            data={
                'sender': '34',
                'receiver_list': '45192278',
                'amount': 100.00,
            },
        )

        expected = {
            'errors': {
                '__all__': [
                    'Not enough funds'
                ]
            }
        }

        self.assertEqual(expected, response.json())

    def test_success(self):
        old_transaction_count = Transaction.objects.count()

        response = self.client.post(
            reverse('index'),
            data={
                'sender': '12',
                'receiver_list': '66904023, 2000139',
                'amount': 50.00,
            },
        )

        expected = {
            'success': True,
        }

        self.assertEqual(expected, response.json())
        self.assertEqual(old_transaction_count + 2, Transaction.objects.count())
        self.assertEqual(25.00, Transaction.objects.get(pk=2).amount)
        self.assertEqual(25.00, Transaction.objects.get(pk=3).amount)
