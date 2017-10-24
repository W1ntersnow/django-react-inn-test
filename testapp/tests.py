from rest_framework.test import APIClient
from django.test import TestCase
from testapp.models import User
from api_v1.views import CashException, NotFoundException


class UserTransferTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.start_cash = 100
        self.transfer_cash = 60
        self.after_writeoff_cash = self.start_cash - self.transfer_cash
        self.url = '/api/1/'

    def set_request_data(self):
        self.request_data = {'username': '0', 'users_inn': self.users_inn_request, 'cash': self.transfer_cash}

    def get_response(self):
        self.response = self.client.put(self.url, self.request_data)

    def check_exc_raise(self, exc=Exception):
        with self.assertRaises(exc):
            self.client.put(self.url, self.request_data)

    def check_response_status(self):
        assert self.response.status_code == 200

    def check_charged_amount(self):
        self.assertEqual(User.objects.filter(pk=1)[0].cash, self.after_writeoff_cash, 'incorrect cash')

    def check_amount_after_transfer(self):
        query_set = User.objects.filter(inn__in=self.users_inn_array)
        transfer_sum = self.transfer_cash/query_set.count()

        for i in query_set:
            self.assertEqual(i.cash, self.start_cash+transfer_sum, 'incorrect cash')

    def prepare_data(self, all_inn='123,234,345,456,567,678,789', req_inn='234,345,456,567,678,789'):
        self.users_inn_all = all_inn
        self.users_inn_request = req_inn
        self.users_inn_array = self.users_inn_request.split(',')
        self.users_inn_len = len(self.users_inn_request.split(','))

        for i, val in enumerate(self.users_inn_all.split(',')):
            User.objects.create(username=str(i), inn=val, cash=self.start_cash)
        self.set_request_data()

    def test_transfer_distinct_inn(self):
        self.prepare_data(all_inn='123,234,345,456,567,678,789', req_inn='234,345,456,567,678,789')
        self.get_response()
        self.check_response_status()
        self.check_charged_amount()
        self.check_amount_after_transfer()

    def test_transfer_with_same_inn(self):
        self.prepare_data(all_inn='123,234,345,456,456,456,456', req_inn='234,345,456')
        self.get_response()
        self.check_response_status()
        self.check_charged_amount()
        self.check_amount_after_transfer()

    def test_transfer_wrong_amount(self):
        self.transfer_cash = 101
        self.prepare_data(all_inn='123,234,345,456,567,678,789', req_inn='234,345,456,567,678,789')
        self.check_exc_raise(CashException)

    def test_transfer_wrong_inn(self):
        self.prepare_data(all_inn='123,234,345,456,567,678,789', req_inn='987,675,344')
        self.check_exc_raise(NotFoundException)
