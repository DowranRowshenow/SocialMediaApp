from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from accounts.models import User
from .forms import FriendRequestForm
from .models import FriendList, FriendRequest


class FriendRequestView(FormView):
    form_class = FriendRequestForm
    template_name = "friends/friend_request_bone.html"

    def form_valid(self, form):
        form.init(self.request.user)
        return super().form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class FriendRequestAcceptView(View):
    
    def get(self, request, email):
        channel_layer = get_channel_layer()
        friend = User.objects.filter(email=email).first()
        if friend:
            friend_request = FriendRequest.objects.filter(sender=friend, receiver=request.user).first()
            friend_request.accept()
            async_to_sync(channel_layer.group_send)(f'friends_{friend_request.sender.username}',{
                "type": "friend_accept",
                "email": friend_request.receiver.email,
                "username": friend_request.receiver.username
            })
        try:
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            return HttpResponseRedirect(reverse('main'))


class FriendRequestDeclineView(View):
    
    def get(self, request, email):
        channel_layer = get_channel_layer()
        friend = User.objects.filter(email=email).first()
        if friend:
            friend_request = FriendRequest.objects.filter(sender=friend, receiver=request.user).first()
            friend_request.decline()
            async_to_sync(channel_layer.group_send)(f'friends_{friend_request.sender.username}',{
                "type": "friend_decline",
                "email": friend_request.receiver.email,
                "username": friend_request.receiver.username
            })
        try:
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            return HttpResponseRedirect(reverse('main'))