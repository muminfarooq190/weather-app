from django.test import TestCase, Client
from core import models
from django.urls import reverse
import requests
from django.contrib.auth import get_user_model


def create_city(user, name='Las Vegas'):
    return models.City.objects.create(name=name, user=user)



class WeatherAppTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='londonapp@dev.com',
            password='pass123'
        )
        self.client = Client()

    # def test_weather_api(self):
    #     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=61e13877b69a6a3fc7f344384e9336fe'
    #     city = 'Las Vegas'
    #     res = requests.get(url.format(city)).json()
    #     self.assertEqual(city, res['name'])

    def test_city_created_successfully(self):
        """Test that city is created with valid payload"""

        city = create_city(self.user)
        self.assertEqual(models.City.objects.count(), 1)

    def test_retrieve_city_successfull(self):
        """Retrieve the city"""

        create_city(self.user)
        create_city(self.user)
        res = self.client.get(reverse('weather:list'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(models.City.objects.count(), 2)

    def test_retrieve_city_limited_user(self):
        """Test the city for authenticated user only"""
        payload = {
            'email': 'mumin@gmail.com',
            'password': 'testpass'
        }
        user = get_user_model().objects.create_user(
            email = payload['email'],
            password = payload['password']
        )
        user_two = get_user_model().objects.create_user(
            email = 'in@gmail.com',
            password = '1234567'
        )
        res = self.client.post(reverse('user:login'), payload)
        self.assertEqual(res.status_code, 200)
        create_city(name='California',user=user)
        create_city(name='LA', user=user_two)
        res = self.client.get(reverse('weather:list'))
        self.assertEqual(res.status_code, 200)
        city = models.City.objects.all().filter(user=user)
        self.assertEqual(len(city), 1)

    def test_create_city_invalid(self):
        """test create city with invalid payload fails"""
        payload = {
            'name': ''
        }
        res = self.client.post(reverse('weather:create'))
        self.assertEqual(res.status_code, 400)
