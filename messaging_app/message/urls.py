from django.urls import path, re_path
from .api import MessageAPI, ChatAPI, DailyMessageAPI, SentMessageAPI, ReceivedMessageAPI

urlpatterns = [
    path('api/message', MessageAPI.as_view()),
    path('api/message/sent', SentMessageAPI.as_view()),
    path('api/message/received', ReceivedMessageAPI.as_view()),
    re_path(r'api/message/chat(?P<target>)', ChatAPI.as_view()),
    re_path(r'api/message/daily(?P<date>)', DailyMessageAPI.as_view()),
]