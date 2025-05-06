from django.shortcuts import render,get_object_or_404
from conversation.models import Conversation, Message

def home(request):
    return render(request, "frontend/home.html")

def get_conversations(request):
    conversations = Conversation.objects.all()
    return render(request, "frontend/conversations.html", {"conversations": conversations})




def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by("timestamp")
    return render(request, "frontend/conversation_detail.html", {"conversation": conversation, "messages": messages})
