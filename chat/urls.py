from django.urls import path
from . import views
from .models import *

urlpatterns = [
    # path('', views.messages_page,name="message"),
    path('news/', views.get_news, name='get_news'),
    path('chat/<int:recipient_id>/', views.chat_view, name='chat'),
    path('send_message/<int:recipient_id>/', views.send_message_view, name='send_message'),
    path ('search/<int:recipient_id>/', views.search, name="search"),
]
