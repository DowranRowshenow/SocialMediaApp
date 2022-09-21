from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q

from .multiform import MultiFormsView
from accounts.models import User
from rooms.models import Message, Room
from posts.models import Post, PostComment
from friends.models import FriendList, FriendRequest
from friends.forms import FriendRequestForm


class MainView(ListView):
    model = FriendList
    template_name = "main/main.html"
    context_object_name = 'friends'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):        
        return super(MainView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        try: friend_list = FriendList.objects.filter(user=self.request.user).first().friends.all()
        except: return None
        return friend_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hash = self.request.GET.get("dm")
        page = self.request.GET.get("page")
        post_hash = self.request.GET.get("pd")
        profile_hash = self.request.GET.get("pv")
        friend = User.objects.filter(hash=hash).first()
        if page:
            context['posts'] = Post.objects.all().order_by("-id")
        elif post_hash:
            post = Post.objects.filter(hash=post_hash).first()
            context['post'] = post
            try: context['comments'] = post.comments.all()
            except: context['comments'] = None
        elif profile_hash:
            context['user'] = User.objects.filter(hash=profile_hash).first()
        elif friend: 
            room = Room.objects.filter(Q(user1=self.request.user,user2=friend) | Q(user1=friend,user2=self.request.user)).first()
            if room:
                context['roomToken'] = room.token
                context['messages'] = Message.objects.filter(room = room).order_by("id")
        context['friend_requests'] = FriendRequest.objects.filter(receiver = self.request.user, is_active=True).order_by('sender__username')
        context['requested_friends'] = FriendRequest.objects.filter(sender = self.request.user, is_active=True).order_by('sender__username')
        return context