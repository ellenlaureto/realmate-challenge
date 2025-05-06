import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, Message


def home(request):
    return HttpResponse("Bem-vindo à página inicial!")


@csrf_exempt
def webhook(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8', errors='ignore'))
        event_type = data.get("type")
        event_data = data.get("data", {})  # Evita erro se 'data' for None
        
        if event_type == "NEW_CONVERSATION": ##EVENTO DE CRIAÇÃO DE CONVERSA##
            conversation = Conversation.objects.create()
            return JsonResponse({"message": "Conversation created", "id": conversation.id}, status=201)

        elif event_type == "NEW_MESSAGE": ##EVENTO DE MENSAGEM RECEBIDA OU ENVIADA##
            if not all(k in event_data for k in ["conversation_id", "direction", "content"]):
                return JsonResponse({"error": "Invalid JSON"}, status=400) 

            conversation_id = event_data.get("conversation_id")
            if not conversation_id or not str(conversation_id).isdigit():
                return JsonResponse({"error": "Invalid Conversation ID"}, status=400)

            conversation = Conversation.objects.filter(id=conversation_id).first()
            if conversation and conversation.status == "OPEN":
                Message.objects.create(
                    conversation=conversation,
                    direction=event_data["direction"],
                    content=event_data["content"],
                    timestamp=event_data.get("timestamp")
                )
                return JsonResponse({"message": "Message added"}, status=201)
            else:
                return JsonResponse({"error": "Cannot add messages to a CLOSED conversation"}, status=400)

        elif event_type == "CLOSE_CONVERSATION": ##EVENTO DE CONVERSA FECHADA##
            conversation = Conversation.objects.filter(id=event_data.get("id")).first()
            if conversation:
                if conversation.status == "CLOSED":
                    return JsonResponse({"error": "This conversation is already CLOSED"}, status=400)

                conversation.status = "CLOSED"
                conversation.save()
                return JsonResponse({"message": "Conversation CLOSED"}, status=200)
        
        return JsonResponse({"error": "Invalid Event"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)



@csrf_exempt
def get_conversation(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    ##EVENTOS DE BUSCA DE CONVERSA##
    conversation = Conversation.objects.filter(id=id).first()
    if not conversation: ##NAO ACHADA##
        return JsonResponse({"error": "Conversation not found"}, status=404)

    messages = list(conversation.messages.values("direction", "content", "timestamp")) ##BUSCA MENSAGENS DA CONVERSA##
    return JsonResponse({
        "id": conversation.id,
        "status": conversation.status,
        "messages": messages
    }, status=200)

