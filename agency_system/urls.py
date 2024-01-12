from django.urls import path
from .views import (index,
                    RegistrationSuccessView,
                    PasswordsChangingView,
                    PasswordChangedSuccessView,
                    TopicListView,
                    TopicDetailView,
                    TopicCreateView,
                    TopicUpdateView,
                    TopicDeleteView,
                    RedactorListView,
                    RedactorDetailView,
                    RedactorCreateView,
                    RedactorUpdateView,
                    NewspaperListView,
                    NewspaperDetailView,
                    NewspaperCreateView,
                    NewspaperUpdateView,
                    )

urlpatterns = [
    path("", index, name="index"),
    path("success/", RegistrationSuccessView.as_view(), name="success"),
    path("redactors/<int:pk>/password/", PasswordsChangingView.as_view(), name="password-update"),
    path("password_changed/", PasswordChangedSuccessView.as_view(), name="password-changed"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", TopicDetailView.as_view(), name="topic-detail"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topics/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path("create_account/", RedactorCreateView.as_view(), name="redactor-create"),
    path("redactors/<int:pk>/edit_profile/", RedactorUpdateView.as_view(), name="redactor-update"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),

]

app_name = "agency_system"
