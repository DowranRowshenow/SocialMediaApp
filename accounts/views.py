import os
from PIL import Image
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse

from accounts.models import User
from accounts.forms import SingUpForm, LogInForm
from .errors import AccountErrors


class IndexView(View):

    def get(self, request):
        link = f"{self.request.build_absolute_uri(reverse('main'))}?{AccountErrors.page}"
        if request.user.is_authenticated: return HttpResponseRedirect(link)
        else: return render(request, 'accounts/index.html')

        
class CustomLoginView(LoginView):
    form_class = LogInForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return f"{self.request.build_absolute_uri(reverse('main'))}?{AccountErrors.page}"


class CustomSignupView(CreateView):
    form_class = SingUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('token')

    def get_success_url(self):
        link = self.request.build_absolute_uri(reverse('verify', args=(self.object.auth_token, )))
        send_verification_mail(self.object, link)
        return super().get_success_url()
        

def send_verification_mail(user, link):
    subject = 'Your accounts need to be verified'
    message = f"Hi click the link to verify your account {link}"
    sender = settings.EMAIL_HOST_USER
    receiver = [user.email]
    send_mail(subject, message, sender, receiver)


class VerifyView(View):

    def get(self, request, token):
        try:
            user = User.objects.filter(auth_token = token).first()
            if user:
                user.is_active = True
                user.save()
                messages.success(request, "Your account is verified.")
                return HttpResponseRedirect(reverse('login'))
        except Exception as e: print(e)
        return HttpResponseRedirect(reverse('error'))


class EditProfileView(UpdateView):
    model = User
    fields = ['image', 'photo', 'first_name', 'last_name', 'bio', 'location', 'gender', 'birth_date']

    def form_valid(self, form):
        image = form.instance.image
        if not image:
            link = f"{self.request.build_absolute_uri(reverse('main'))}?{AccountErrors.page}&{AccountErrors.c10ae}"
            return HttpResponseRedirect(link)
        else:    
            if image.size > 4*1024*1024:
                link = f"{self.request.build_absolute_uri(reverse('main'))}?{AccountErrors.page}&{AccountErrors.c95ae}"
                return HttpResponseRedirect(link)
            try:
                # Thumbnail
                THUMBNAIL_SIZE = (160, 160)  # dimensions
                picture = Image.open(image)
                # Convert to RGB if necessary
                if picture.mode not in ('L', 'RGB'): picture = picture.convert('RGB')
                # Create a thumbnail and use antialiasing for a smoother thumbnail
                picture.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
                # Fetch image into memory
                temp_handle = BytesIO()
                picture.save(temp_handle, 'png')
                temp_handle.seek(0)
                # Remove old image
                if self.request.user.image.name != "profile.png":
                    try: os.remove(self.request.user.image.path)
                    except: pass
                if self.request.user.photo.name != "profile.png":
                    try: os.remove(self.request.user.photo.path)
                    except: pass
                # Rename new image
                if self.request.user.image.name.rpartition('/')[-1] == f"{self.request.user.username}.png":
                    image.name = f"{self.request.user.username}2.png"
                else:
                    image.name = f"{self.request.user.username}.png"
                # Save new image
                file_name, file_ext = os.path.splitext(image.name.rpartition('/')[-1])
                suf = SimpleUploadedFile(file_name + file_ext, temp_handle.read(), content_type='image/png')
                form.instance.photo = suf
            except:
                link = f"{self.request.build_absolute_uri(reverse('main'))}?{AccountErrors.page}&{AccountErrors.c47ae}"
                return HttpResponseRedirect(link)
        self.object = form.save()
        return HttpResponseRedirect(f"{reverse('main')}?{AccountErrors.page}")

    def form_invalid(self, form):
        link = f"{self.request.build_absolute_uri(reverse('main'))}?{AccountErrors.page}&{AccountErrors.c71ae}"
        return HttpResponseRedirect(link)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))