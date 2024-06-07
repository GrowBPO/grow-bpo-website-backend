from django.urls import path
from bi_report.views import *

urlpatterns = [
    path('user-company/<int:user_id>/', UserCompanyView.as_view(), name="api-user-company"),
]

