from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('',views.ListWeatherView.as_view(), name='list'),
    path('create/city/', views.CreateCityView.as_view(), name='create')
]
