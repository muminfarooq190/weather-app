from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView
)
from core import models
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

class ListWeatherView(ListView, LoginRequiredMixin):
    model = models.City
    template_name = 'weather_list.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=61e13877b69a6a3fc7f344384e9336fe'

        cities = models.City.objects.all()
        weather_data = []
        for city in cities:
            city_weather = requests.get(url.format(city)).json()
             #request the API data and convert the JSON to Python data types
            weather = {
                'city' : city,
                'temperature' : city_weather['main']['temp'],
                'description' : city_weather['weather'][0]['description'],
                'icon' : city_weather['weather'][0]['icon']
            }
            weather_data.append(weather)
        context = {'weather_data' : weather_data}
        return context

    queryset = models.City.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).latest('id')

class CreateCityView(CreateView, LoginRequiredMixin):
    form_class = forms.UserCreationForm
    template_name = 'create_city.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            ## Assuming that the relevant field is named user,
            ##it will save the user accessing the form using request.user
            obj.save()
            return redirect('weather:list')
        return render(request, self.template_name, {'form': form}, status=400)


def welcome(request):
    return render(request, 'welcome.html')
