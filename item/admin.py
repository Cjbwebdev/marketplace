from django.contrib import admin
from .models import Category, Item
from conversation.models import Conversation, ConversationMessage

# Registering models from the current app
admin.site.register(Category)
admin.site.register(Item)

# Registering models from the 'conversation' app
admin.site.register(Conversation)
admin.site.register(ConversationMessage)
