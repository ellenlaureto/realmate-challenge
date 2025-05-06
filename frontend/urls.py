from django.urls import path
from .views import get_conversations, conversation_detail,home

urlpatterns = [
    path("", home, name="home"),
    path("get-conversations/", get_conversations, name="get_conversations"),
    path("conversation/<int:conversation_id>/", conversation_detail, name="conversation_detail"),
]
