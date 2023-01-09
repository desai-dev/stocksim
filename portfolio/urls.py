from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('interact/', views.interact, name="interact")
]