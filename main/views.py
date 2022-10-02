from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q

from accounts.models import User
from rooms.models import Message, Room
from posts.models import Post, PostComment
from friends.models import FriendList, FriendRequest


class MainView(ListView):
    template_name = "main/main.html"
    context_object_name = 'item_list'
    paginate_by = 10

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):        
        return super(MainView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        dm_hash = self.request.GET.get("dm")
        friend = User.objects.filter(hash=dm_hash).first()
        page = self.request.GET.get("pg")
        post_hash = self.request.GET.get("pd")
        profile_hash = self.request.GET.get("pv")
        queryset = list()
        if friend:
            self.paginate_by = 100
            room = Room.objects.filter(Q(user1=self.request.user,user2=friend) | Q(user1=friend,user2=self.request.user)).first()
            if room: queryset = Message.objects.filter(room = room).order_by("id")
        elif page == 'posts':
            queryset = Post.objects.all().order_by("-id")
        elif post_hash:
            self.paginate_by = 100
            queryset = Post.objects.filter(hash=post_hash).first().comments.all()
        elif profile_hash:
            user = User.objects.filter(hash=profile_hash).first()
            queryset = Post.objects.filter(user=user).order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hash = self.request.GET.get("dm")
        post_hash = self.request.GET.get("pd")
        profile_hash = self.request.GET.get("pv")
        friend = User.objects.filter(hash=hash).first()
        if post_hash:
            post = Post.objects.filter(hash=post_hash).first()
            context['post'] = post
        elif profile_hash:
            context['user'] = User.objects.filter(hash=profile_hash).first()
        elif friend: 
            room = Room.objects.filter(Q(user1=self.request.user,user2=friend) | Q(user1=friend,user2=self.request.user)).first()
            if room: context['roomToken'] = room.token
        try: context['friends'] = FriendList.objects.filter(user=self.request.user).first().friends.all()
        except: context['friends'] = list()
        context['friend_requests'] = FriendRequest.objects.filter(receiver = self.request.user, is_active=True).order_by('sender__username')
        context['requested_friends'] = FriendRequest.objects.filter(sender = self.request.user, is_active=True).order_by('sender__username')
        return context