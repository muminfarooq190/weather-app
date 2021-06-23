from django.views.generic import (
    CreateView, UpdateView, ListView, DeleteView
)
from django.shortcuts import render
from django.urls import reverse
from core import models
from .forms import UserCreationForm
from django.views.generic import View



class CreateUserView(View):
    form_class = UserCreationForm
    template_name = 'index.html'
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
              form.save()

        return render(request, self.template_name, {'form': form})
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

def baseview(request):
    return render(request, 'base.html')
