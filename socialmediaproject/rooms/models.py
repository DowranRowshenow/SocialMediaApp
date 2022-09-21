from django.db import models

from socialmediaproject import settings


class Room(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user2', on_delete=models.CASCADE)
    token = models.CharField(null=False, blank=False, unique=True, max_length=255)

    def __str__(self):
        return self.token


class Message(models.Model):
	room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
	content = models.TextField(blank=False, null=False)
	is_seen = models.BooleanField(default=False)
	sent_date_time = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = (
			'sent_date_time',
		)

	def __str__(self):
		return self.sender.email