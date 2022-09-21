from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('signup/', views.CustomSignupView.as_view(), name="signup"),
    path('verify/<token>', views.VerifyView.as_view(), name='verify'),
    path('token/', 
        TemplateView.as_view(template_name = 'accounts/token.html'), 
        name="token"
    ),
    path('success/', 
        TemplateView.as_view(template_name = 'accounts/success.html'), 
        name="success"
    ),
    path('error/', 
        TemplateView.as_view(template_name = 'accounts/error.html'), 
        name='error'
    ),
    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
        name='reset_password'
    ),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/token.html'), 
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/new_password.html'), 
        name='password_reset_confirm'
    ),
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/success.html'), 
        name='password_reset_complete'
    ),
    path('<pk>/edit_profile/', views.EditProfileView.as_view(), name="edit_profile"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
]