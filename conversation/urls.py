from django.urls import path
from .views import conversation_view
from . import views
app_name = 'conversation'

urlpatterns = [
    path('', conversation_view, name='inbox'),  # Default path for the inbox view
    path('new/<int:item_pk>/', conversation_view, name='new'),  # Path to create a new conversation
]
