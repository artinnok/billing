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

    @patch('core.forms.Profile')
    def test_some_users_not_found(self, mock):
        mock.objects.all.return_value.values_list.return_value = [
            ('45192278', '45192278'),
        ]

        response = self.client.post(
            reverse('index'),
            data={
                'sender': '45192278',
                'receiver_list': '1, 2',
                'amount': 10.00,
            },
        )

        expected = {
            'receiver_list': [
                "Users with this INN ['1', ' 2'] not found"
            ]
        }

        self.assertEqual(expected, response.json())

    def test_profile_not_found(self):
        response = self.client.post(
            reverse('index'),
            data={
                'sender': '10',
                'receiver_list': '45192278',
                'amount': 10.00,
            },
        )

        expected = {
            'errors': {
                'sender': [
                    'Select a valid choice. 10 is not one of the available choices.'
                ]
            }
        }

        self.assertEqual(expected, response.json())

    @patch('core.forms.Profile')
    def test_not_enough_funds(self, mock):
        mock.objects.all.return_value.values_list.return_value = [
            ('387068077', '387068077'),
        ]
        mock.objects.filter.return_value.values_list.return_value = ['45192278']
        mock.objects.get.return_value.balance = 10.00
        mock.DoesNotExist = ObjectDoesNotExist

        response = self.client.post(
            reverse('index'),
            data={
                'sender': '387068077',
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
                'sender': '66904023',
                'receiver_list': '66904023',
                'amount': 10.00,
            },
        )

        expected = {
            'success': True,
        }

        self.assertEqual(old_transaction_count + 1, Transaction.objects.count())
        self.assertEqual(expected, response.json())
