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


class IndexView(View):

    def get(self, request):
        link = self.request.build_absolute_uri(reverse('main')) + '?page=profile'
        if request.user.is_authenticated: return HttpResponseRedirect(link)
        else: return render(request, 'accounts/index.html')

        
class CustomLoginView(LoginView):
    form_class = LogInForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return self.request.build_absolute_uri(reverse('main')) + '?page=profile'


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
    message = 'Hi click the link to verify your account ' + link
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
    fields = ['image']

    def form_valid(self, form):
        image = form.instance.image
        self.object = form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        link = self.request.build_absolute_uri(reverse('main')) + '?page=p'
        return HttpResponseRedirect(link)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))