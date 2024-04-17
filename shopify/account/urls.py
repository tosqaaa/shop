from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .forms import LoginForm
from .views import dashboard, register, edit, delete

appname = 'account'
urlpatterns = [
    path('', dashboard, name='home'),

    path('login/', auth_views.LoginView.as_view(form_class=LoginForm, template_name='account/registration/login.html', success_url=reverse_lazy('account:dashboard')),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/registration/logged_out.html'), name='logout'),

    # смена пароля
    path('password-change/',
         auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done'), template_name='account/registration/password_change_form.html'),
         name='password_change'),
    path('password-change/done', auth_views.PasswordChangeDoneView.as_view(template_name='account/registration/password_change_done.html'), name='password_change_done'),

    # сброс пароля
    path('password-reset/', auth_views.PasswordResetView.as_view(
         template_name="account/registration/password_reset_form.html",
         email_template_name='account/registration/password_reset_email.html',
         success_url=reverse_lazy("account:password_reset_done")),
         name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='account/registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('account:password_reset_complete'), template_name='account/registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/registration/password_reset_complete.html'), name='password_reset_complete'),

    # регистрация
    path('register/', register, name='register'),

    # редактирования профиля
    path('delete/', delete, name='delete'),
]
