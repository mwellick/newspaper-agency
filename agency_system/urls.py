from django.urls import path
from agency_system.views import index
from .views import (TopicListView,
                    TopicDetailView,
                    RedactorListView,
                    RedactorDetailView,
                    NewspaperListView,
                    NewspaperDetailView)

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", TopicDetailView.as_view(), name="topic-detail"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),

]

app_name = "agency_system"
