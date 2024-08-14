from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation

def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # Redirect if the user is the creator of the item
    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Check for existing conversations
    conversations = Conversation.objects.filter(item=item, members__in=[request.user.id])
    if conversations.exists():
        # Redirect to the existing conversation (assuming you have a URL named 'conversation:detail')
        return redirect('conversation:detail', pk=conversations.first().pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            # Create a new conversation
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            # Create and save the conversation message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation  # Fixed typo here
            conversation_message.created_by = request.user
            conversation_message.save()

            # Redirect to item detail page after creating the conversation
            return redirect('items:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form,
        'item': item  # You might want to pass the item to the template for context
    })
