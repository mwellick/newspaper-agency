from django.urls import path
from agency_system.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "agency_system"
