from django import forms
from django.db.models import Q
from django.utils.translation import gettext as _

from accounts.models import User
from .models import FriendRequest


class FriendRequestForm(forms.Form):
    email = forms.EmailField()

    def init(self, user): 
        email = self.cleaned_data.get("email")
        friend = User.objects.filter(email=email).first()
        if friend:
            if friend != user:
                request = FriendRequest.objects.filter(Q(sender=user, receiver=friend) | Q(sender=friend, receiver=user)).first()
                if not request:
                    friend_request = FriendRequest.objects.create(sender=user, receiver=friend)
                    self.add_error("email", _("Friend request sent successfully."))
                elif request.is_active and request.sender == user:
                    self.add_error("email", _("You have already sent this user a friend request."))
                elif not request.is_active:
                    self.add_error("email", _("You are already friends with this user"))
                else:
                    self.add_error("email", _("You already have a friend request from this user"))
            else:
                self.add_error("email", _("You cannot send yourself a friend request."))
        else:
            self.add_error("email", _("Please enter a valid email address."))