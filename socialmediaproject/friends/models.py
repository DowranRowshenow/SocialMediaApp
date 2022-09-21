import uuid
from django.db import models

from socialmediaproject import settings
from rooms.models import Room


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.email

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, friend):
        self.remove_friend(friend)
        friends_list = FriendList.objects.get(user=friend)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_receiver")
    is_active = models.BooleanField(default=True, blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.email

    def accept(self):
        receiver_friend_list = FriendList.objects.filter(user=self.receiver).first()
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
        else:
           receiver_friend_list = FriendList.objects.create(user=self.receiver)
           receiver_friend_list.add_friend(self.sender)
        sender_friend_list = FriendList.objects.filter(user=self.sender).first()
        if sender_friend_list:
            sender_friend_list.add_friend(self.receiver)
        else:
            sender_friend_list = FriendList.objects.create(user=self.sender)
            sender_friend_list.add_friend(self.receiver)
        Room.objects.create(user1=self.sender, user2=self.receiver, token=str(uuid.uuid4()))
        self.is_active = False
        self.save()
        
    def decline(self):
        self.delete()

    def cancel(self):
        self.delete()