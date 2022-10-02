import uuid
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .models import Post, PostComment
from .errors import PostErrors


class CreatePostView(CreateView):
    model = Post
    fields = ['content', 'image']

    def form_valid(self, form):
        image = form.instance.image
        content = form.instance.content
        if not image and not content:
            return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}&{PostErrors.c10pc}")
        if image:
            if image.size > 4*1024*1024:
                return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}&{PostErrors.c95pc}")
        form.instance.user = self.request.user
        form.instance.hash = uuid.uuid4()
        if image: image.name = f"{form.instance.hash}.png"
        self.object = form.save()
        return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}")

    def form_invalid(self, form):
        return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}&{PostErrors.c71pc}")


class EditPostView(UpdateView):
    model = Post
    fields = ['content', 'image']

    def form_valid(self, form):
        image = form.instance.image
        content = form.instance.content
        self.object = self.get_object()
        if not image and not content:
            return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}&{PostErrors.c10pe}&pk={self.object.pk}")
        if image:
            if image.size > 4*1024*1024:
                return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}&{PostErrors.c95pe}&pk={self.object.pk}")
            if image.size != self.object.image.size:
                try:
                    try: os.remove(self.object.image.path)
                    except: return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}")
                    image.name = f"{self.object.hash}.png"
                except:
                    return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}&{PostErrors.c47pe}&pk={self.object.pk}")
        self.object = form.save()
        return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}")

    def form_invalid(self, form):
        return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}&{PostErrors.c71pe}&pk={self.object.pk}")
    

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
        return f"{reverse('main')}?{PostErrors.page}"