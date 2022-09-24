from pydoc import pager
import uuid
import os
from PIL import Image
from io import BytesIO

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
            link = f"{self.request.build_absolute_uri(reverse('main'))}?{PostErrors.page}&{PostErrors.c10pc}"
            return HttpResponseRedirect(link)
        if image:
            if image.size > 4*1024*1024:
                link = f"{self.request.build_absolute_uri(reverse('main'))}?{PostErrors.page}&{PostErrors.c95pc}"
                return HttpResponseRedirect(link)
        form.instance.user = self.request.user
        form.instance.hash = uuid.uuid4()
        self.object = form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        link = f"{self.request.build_absolute_uri(reverse('main'))}?{PostErrors.page}&{PostErrors.c71pc}"
        return HttpResponseRedirect(link)


class EditPostView(UpdateView):
    model = Post
    fields = ['content', 'image']

    def form_valid(self, form):
        image = form.instance.image
        content = form.instance.content
        self.object = self.get_object()
        if not image and not content:
            link = f"{self.request.build_absolute_uri(reverse('main'))}?{PostErrors.page}&{PostErrors.c10pe}"
            return HttpResponseRedirect(link)
        if image:
            if image.size > 4*1024*1024:
                link = f"{self.request.build_absolute_uri(reverse('main'))}?{PostErrors.page}&{PostErrors.c95pe}"
                return HttpResponseRedirect(link)
            try:
                # Remove old image
                try: os.remove(self.object.image.path)
                except: return HttpResponseRedirect(f"{reverse('main')}?{PostErrors.page}")
                # Rename new image
                image.name = f"{self.object.hash}.png"
            except:
                link = f"{self.request.build_absolute_uri(reverse('main'))}?{PostErrors.page}&{PostErrors.c47pe}"
                return HttpResponseRedirect(link)
        self.object = form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        link = f"{self.request.build_absolute_uri(reverse('main'))}?{PostErrors.page}&{PostErrors.c71pe}"
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
        return f"{self.request.build_absolute_uri(reverse('main'))}?{PostErrors.page}"