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
    conversations = Conversation.objects.filter(item=item, members=request.user)
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

            # Create and save the conversation message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # Redirect to the newly created conversation detail page
            return redirect('conversation:detail', pk=conversation.pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form,
        'item': item
    })

def inbox(request):
    # Fetch conversations where the current user is a member
    conversations = Conversation.objects.filter(members=request.user)
    
    return render(request, 'conversation/new.html', {
        'conversations': conversations
    })