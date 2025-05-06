from django.db import models

# Create your models here.

class Conversation(models.Model):
    STATUS_CHOICE = [('OPEN','Open'), ('CLOSED','Closed'),]
    id = models.AutoField(primary_key=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICE,default='OPEN')
    timestamp = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    TYPE_CHOICE = [('SENT','Sent'), ('RECEIVED','Received'),]

    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    direction = models.CharField(max_length=10, choices=TYPE_CHOICE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
