from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class YourAPITestCase(APITestCase):
    def test_invalid_products_type(self):
        data = {
            "products": "HelloWorld",
            "firstname": "Иван",
            "lastname": "Петров",
            "phonenumber": "+79291000000",
            "address": "Москва"
        }
        response = self.client.post(reverse('foodcartapp:order'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('products', response.data)

    def test_null_products(self):
        data = {
            "products": None,
            "firstname": "Иван",
            "lastname": "Петров",
            "phonenumber": "+79291000000",
            "address": "Москва"
        }
        response = self.client.post(reverse('foodcartapp:order'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('products', response.data)

    def test_empty_products_list(self):
        data = {
            "products": [],
            "firstname": "Иван",
            "lastname": "Петров",
            "phonenumber": "+79291000000",
            "address": "Москва"
        }
        response = self.client.post(reverse('foodcartapp:order'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_products(self):
        data = {
            "firstname": "Иван",
            "lastname": "Петров",
            "phonenumber": "+79291000000",
            "address": "Москва"
        }
        response = self.client.post(reverse('foodcartapp:order'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_null_firstname(self):
        data = {
            "products": [{"product": 1, "quantity": 1}],
            "firstname": None,
            "lastname": "Петров",
            "phonenumber": "+79291000000",
            "address": "Москва"
        }
        response = self.client.post(reverse('foodcartapp:order'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('firstname', response.data)

    def test_missing_keys(self):
        data = {
            "products": [{"product": 1, "quantity": 1}]
        }
        response = self.client.post(reverse('foodcartapp:order'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('firstname', response.data)
        self.assertIn('lastname', response.data)
        self.assertIn('phonenumber', response.data)
        self.assertIn('address', response.data)

    def test_invalid_firstname_type(self):
        data = {
            "products": [{"product": 1, "quantity": 1}],
            "firstname": [],
            "lastname": "Петров",
            "phonenumber": "+79291000000",
            "address": "Москва"
        }
        response = self.client.post(reverse('foodcartapp:order'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('firstname', response.data)
