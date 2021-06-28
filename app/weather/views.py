from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView
)
from core import models
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

class ListWeatherView(ListView, LoginRequiredMixin):
    model = models.City
    template_name = 'weather_list.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=61e13877b69a6a3fc7f344384e9336fe'

        cities = models.City.objects.filter(user=self.request.user)
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



    # def get_queryset(self):
    #     try:
    #         self.queryset = models.City.objects.all()
    #         if self.queryset.exists():
    #             return self.queryset.filter(user=self.request.user).latest('-id')
    #     except (models.City.DoesNotExist):
    #         pass


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


def getweatherofcity(city):
    print("*********************", city)
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=61e13877b69a6a3fc7f344384e9336fe'
    city_weather = requests.get(url.format(city)).json()
     #request the API data and convert the JSON to Python data types
    weather = {
        'city' : city,
        'temperature' : city_weather['main']['temp'],
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }
    return weather



@login_required
def searchforcity(request):
    form = forms.SearchForm()
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            weather = getweatherofcity(request.POST.get("city"))
            return render(request, 'city_info.html', {'weather':weather})
        else:
            if not request.POST.get('city').isdigit():
                weather = getweatherofcity(request.POST.get("city"))
                return render(request, 'city_info.html', {'weather':weather})
            return HttpResponse("Your form is not valid")
    return render(request, 'search_city.html',{'form':form})
