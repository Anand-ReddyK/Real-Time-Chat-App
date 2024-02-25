from django.db import models
import uuid

from django.core.exceptions import ValidationError

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 30, unique=True)
    rooms = models.ManyToManyField('Room', blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    def __str__(self) -> str:
        return self.name



class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("You cannot send a friend request to your self")
        
        if  self.from_user in self.to_user.friends.all():
            raise ValidationError("You cannot send a friend request to your friend")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(FriendRequest, self).save(*args, **kwargs)



class Room(models.Model):
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    room_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def get_room_name(self, user):
        room_name = [member.name for member in self.members.all() if member != user]
        return ",".join(room_name)


class Messages(models.Model):
    conversation = models.ForeignKey(Room, related_name="conversation", on_delete=models.CASCADE)
    content = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)
    
    def clean(self):
        if self.created_by not in self.conversation.members.all():
            raise ValidationError("The user is not a member of this group")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Messages, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.content
