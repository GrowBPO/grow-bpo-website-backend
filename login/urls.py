from django.urls import path
from login.views import *

urlpatterns = [
    path('user', UserView.as_view(), name="api-user"),
    path('user/check', CheckAuthView.as_view(), name="api-user"),
    path('login', LoginView.as_view(), name="api-login"),
    path('logout', LogoutView.as_view(), name="api-logout"),
    path('redefine-password/', RedefinePasswordView.as_view(), name='redefine_password'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
]

