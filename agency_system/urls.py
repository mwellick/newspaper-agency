from django.urls import path
from .views import (
    index,
    TopicListView,
    TopicDetailView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
    RedactorListView,
    RedactorDetailView,
    RedactorCreateView,
    RedactorUpdateView,
    RedactorDeleteView,
    NewspaperListView,
    NewspaperDetailView,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    RegistrationSuccessView,
    PasswordsChangingView,
    PasswordChangedSuccessView,
    PasswordsResettingView,
    PasswordResettingConfirmView,
    PasswordResetSuccess,
    AddCommentView,
    CommentUpdateView,
    CommentDeleteView,
    ReplyCommentView,
    CommentAndRepliesView,
    ReplyUpdateView,
    ReplyDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", TopicDetailView.as_view(), name="topic-detail"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topics/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path("create_account/", RedactorCreateView.as_view(), name="redactor-create"),
    path(
        "redactors/<int:pk>/edit_profile/",
        RedactorUpdateView.as_view(),
        name="redactor-update",
    ),
    path(
        "redactors/<int:pk>/delete_profile/",
        RedactorDeleteView.as_view(),
        name="redactor-delete",
    ),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path(
        "newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"
    ),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path(
        "newspapers/<int:pk>/update/",
        NewspaperUpdateView.as_view(),
        name="newspaper-update",
    ),
    path(
        "newspapers/<int:pk>/delete/",
        NewspaperDeleteView.as_view(),
        name="newspaper-delete",
    ),
    path(
        "registration/success/",
        RegistrationSuccessView.as_view(),
        name="registration-success",
    ),
    path(
        "redactors/<int:pk>/password/",
        PasswordsChangingView.as_view(),
        name="password-update",
    ),
    path(
        "passwords/changed/",
        PasswordChangedSuccessView.as_view(),
        name="password-changed",
    ),
    path("passwords/reset/", PasswordsResettingView.as_view(), name="password-reset"),
    path(
        "passwords/reset/<uidb64>/token/",
        PasswordResettingConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "accounts/reset/done/",
        PasswordResetSuccess.as_view(),
        name="password-reset-success",
    ),
    path(
        "newspapers/<int:pk>/comment/", AddCommentView.as_view(), name="comment-create"
    ),
    path(
        "newspapers/<int:pk>/comments/<int:comment_id>/reply",
        ReplyCommentView.as_view(),
        name="reply-comment" "-create",
    ),
    path(
        "comments/<int:pk>/replies",
        CommentAndRepliesView.as_view(),
        name="comment-and-replies",
    ),
    path(
        "comments/<int:pk>/update", CommentUpdateView.as_view(), name="comment-update"
    ),
    path(
        "comments/<int:pk>/with/replies/delete",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path("replies/<int:pk>/update", ReplyUpdateView.as_view(), name="reply-update"),
    path("replies/<int:pk>/delete", ReplyDeleteView.as_view(), name="reply-delete"),
]

app_name = "agency_system"
