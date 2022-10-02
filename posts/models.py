import os
from django.db import models
from django.dispatch import receiver

from socialmediaproject import settings


class PostComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_comment_user', on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    sent_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Post(models.Model):
    hash = models.CharField(max_length=36, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_user', on_delete=models.CASCADE)
    content = models.TextField(max_length=250, blank=True)
    comments = models.ManyToManyField(PostComment, blank=True, related_name="comments")
    image = models.ImageField(upload_to='uploads/posts/', blank=True)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_liked_user')
    disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_disliked_user')
    update_date_time = models.DateTimeField(auto_now=True)
    created_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def add_comment(self, comment):
        self.comments.add(comment)

    def add_liked_user(self, account):
        if not account in self.liked_users.all():
            if not account in self.disliked_users.all():
                self.liked_users.add(account)
            else:
                self.disliked_users.remove(account)
                self.liked_users.add(account)
        else:
            if not account in self.disliked_users.all():
                self.liked_users.remove(account)
            else:
                self.disliked_users.remove(account)
                self.liked_users.add(account)

    def add_disliked_user(self, account):
        if not account in self.disliked_users.all():
            if not account in self.liked_users.all():
                self.disliked_users.add(account)
            else:
                self.liked_users.remove(account)
                self.disliked_users.add(account)
        else:
            if not account in self.liked_users.all():
                self.disliked_users.remove(account)
            else:
                self.liked_users.remove(account)
                self.disliked_users.add(account)
        
        
@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image: 
        if os.path.isfile(instance.image.path): 
            os.remove(instance.image.path)