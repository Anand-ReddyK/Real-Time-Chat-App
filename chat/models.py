from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30, unique=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self) -> str:
        return self.name


class SingleChat(models.Model):
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)


class Messages(models.Model):
    conversation = models.ForeignKey(SingleChat, related_name="conversation", on_delete=models.CASCADE)
    content = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)
    

    def __str__(self) -> str:
        return self.content
