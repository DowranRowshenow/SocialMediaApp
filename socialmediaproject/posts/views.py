import uuid
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .models import Post, PostComment


class CreatePostView(CreateView):
    model = Post
    fields = ['content', 'image']

    def form_valid(self, form):
        image = form.instance.image
        content = form.instance.content
        if not image and not content:
            link = self.request.build_absolute_uri(reverse('main')) + '?page=w'
            return HttpResponseRedirect(link)
        if image:
            if image.size > 4*1024*1024:
                link = self.request.build_absolute_uri(reverse('main')) + '?page=x'
                return HttpResponseRedirect(link)
        form.instance.user = self.request.user
        form.instance.hash = uuid.uuid4()
        self.object = form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        link = self.request.build_absolute_uri(reverse('main')) + '?page=y'
        return HttpResponseRedirect(link)


class EditPostView(UpdateView):
    model = Post
    fields = ['content', 'image']

    def form_valid(self, form):
        image = form.instance.image
        content = form.instance.content
        if not image and not content:
            link = self.request.build_absolute_uri(reverse('main')) + '?page=w'
            return HttpResponseRedirect(link)
        self.object = form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        link = self.request.build_absolute_uri(reverse('main')) + '?page=z'
        return HttpResponseRedirect(link)
    

class LikePostView(View):

    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        post.add_liked_user(self.request.user)
        return redirect(self.request.META.get('HTTP_REFERER'))


class DislikePostView(View):

    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        post.add_disliked_user(self.request.user)
        return redirect(self.request.META.get('HTTP_REFERER'))


class DeletePostView(DeleteView):
    model = Post

    def get_success_url(self):
        return self.request.build_absolute_uri(reverse('main')) + '?page=posts'