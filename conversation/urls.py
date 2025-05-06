from django.urls import path
from .views import webhook, get_conversation,home

urlpatterns = [
    path('webhook/', webhook, name="webhook"),
    path('conversations/<int:id>/', get_conversation, name="get_conversation"),
]
