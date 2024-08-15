from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation

def conversation_view(request, item_pk=None):
    if item_pk:
        # Handle new conversation creation
        item = get_object_or_404(Item, pk=item_pk)

        # Redirect if the user is the creator of the item
        if item.created_by == request.user:
            return redirect('dashboard:index')

        # Check for existing conversations
        conversations = Conversation.objects.filter(item=item, members=request.user)
        if conversations.exists():
            # Redirect to the inbox
            return redirect('conversation:inbox')

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
                conversation_message.conversation = conversation
                conversation_message.created_by = request.user
                conversation_message.save()

                # Redirect to the inbox after creating the conversation
                return redirect('item:detail', pk=item_pk)
        else:
            form = ConversationMessageForm()

        # Render the form to start a new conversation along with the item details
        return render(request, 'conversation/new.html', {
            'form': form,
            'item': item,
            'conversations': None  # No conversations to list if creating a new one
        })

    else:
        # Handle the inbox view
        # Fetch conversations where the current user is a member
        conversations = Conversation.objects.filter(members=request.user)

        # Render the template to display the list of conversations and the form
        return render(request, 'conversation/new.html', {
            'form': ConversationMessageForm(),  # Empty form to start a new conversation
            'item': None,  # No item to show in the inbox view
            'conversations': conversations
        })
