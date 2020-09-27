from django.urls import path
from .api import MessageAPI, ChatAPI, DailyMessageAPI, SentMessageAPI, ReceivedMessageAPI

urlpatterns = [
    path('api/message', MessageAPI.as_view()),
    path('api/message/sent', SentMessageAPI.as_view()),
    path('api/message/received', ReceivedMessageAPI.as_view()),
    path('api/message/<str:target>', ChatAPI.as_view()),   
    path('api/message/daily/<str:date_str>', DailyMessageAPI.as_view()),   
]