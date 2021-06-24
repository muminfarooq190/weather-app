from django.shortcuts import render
from django.views.generic import (
    ListView, CreateView
)
from core import models
from . import forms

class ListWeatherView(ListView):
    model = models.City
    template_name = 'weather_list.html'
    queryset = models.City.objects.all()

    def get_queryset(self):
        return self.queryset.all()


class CreateCityView(CreateView):
    form_class = forms.UserCreationForm
    template_name = 'create_city.html'
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
              form.save()


        return render(request, self.template_name, {'form': form}, status=400)
