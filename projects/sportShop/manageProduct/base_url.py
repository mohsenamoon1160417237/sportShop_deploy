from django.urls import path

from .views.base import base_view

urlpatterns = [

    path('', base_view),
]
