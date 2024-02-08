from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .forms import (RedactorCreationForm,
                    RedactorEditForm,
                    PasswordChangingForm,
                    PasswordResettingForm,
                    PasswordResettingFormConfirm,
                    CommentForm,
                    ReplyCommentForm,
                    TopicSearchForm,
                    RedactorSearchForm,
                    NewspaperSearchForm
                    )
from .models import Topic, Redactor, Newspaper, Comment, ReplyComment


def index(request: HttpRequest) -> HttpResponse:
    nature_topics = Topic.objects.filter(name="Nature")
    sport_topics = Topic.objects.filter(name="Sport")
    travel_topics = Topic.objects.filter(name="Travel")
    video_games_topics = Topic.objects.filter(name="Video Games")
    business_topics = Topic.objects.filter(name="Business")
    movies_topics = Topic.objects.filter(name="Movies")
    num_topics = Topic.objects.count()
    latest_news_list = Newspaper.objects.order_by("-published_date")[:3]
    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    context = {
        "num_topics": num_topics,
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "latest_news_list": latest_news_list,
        "nature_topics": nature_topics,
        "sport_topics": sport_topics,
        "travel_topics": travel_topics,
        "video_games_topics": video_games_topics,
        "business_topics": business_topics,
        "movies_topics": movies_topics,

    }
    return render(request, "agency_system/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 6
    context_object_name = "topic_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        topic_name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(
            initial={"name": topic_name}
        )
        return context

    def get_queryset(self):
        queryset = Topic.objects.all()
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__startswith=form.cleaned_data["name"])
        return queryset.none()


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic
    context_object_name = "topic"


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency_system:topic-list")
    template_name = "agency_system/topic_form.html"


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency_system:topic-list")
    template_name = "agency_system/topic_form.html"


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    template_name = "agency_system/topic_confirm_delete.html"
    success_url = reverse_lazy("agency_system:topic-list")
    context_object_name = "topic"


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__startswith=form.cleaned_data["username"])
        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor


class RedactorCreateView(generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("agency_system:registration-success")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorEditForm
    template_name = "registration/edit_profile.html"
    context_object_name = "redactor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return_url"] = reverse_lazy("agency_system:redactor-detail", kwargs={"pk": self.kwargs["pk"]})
        return context

    def get_success_url(self):
        return reverse_lazy("agency_system:redactor-detail", kwargs={"pk": self.object.pk})


class RedactorDeleteView(generic.DeleteView):
    model = Redactor
    template_name = "agency_system/redactor_confirm_delete.html"
    success_url = reverse_lazy("login")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        news_title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(
            initial={"title": news_title}
        )
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.all()
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments_number = Comment.objects.filter(post_comment=self.object).count()
        context["comments_number"] = comments_number
        return context


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("agency_system:newspaper-list")
    template_name = "agency_system/newspaper_form.html"


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    template_name = "agency_system/newspaper_update.html"

    def get_success_url(self):
        updated_news_id = self.kwargs["pk"]
        edited_news = Newspaper.objects.get(id=updated_news_id)
        news_id = edited_news.id
        return reverse_lazy("agency_system:newspaper-detail", kwargs={"pk": news_id})


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    template_name = "agency_system/newspaper_confirm delete.html"
    success_url = reverse_lazy("agency_system:newspaper-list")


class RegistrationSuccessView(TemplateView):
    template_name = 'registration/registration_success.html'


class PasswordChangedSuccessView(TemplateView):
    template_name = "registration/password_changed_success.html"


class PasswordsChangingView(PasswordChangeView):
    model = Redactor
    form_class = PasswordChangingForm
    success_url = reverse_lazy("agency_system:password-changed")
    template_name = "registration/password_change.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return_url"] = reverse_lazy("agency_system:redactor-detail", kwargs={"pk": self.kwargs["pk"]})
        return context


class PasswordsResettingView(PasswordResetView):
    model = Redactor
    form_class = PasswordResettingForm
    success_url = reverse_lazy("agency_system:password-reset")
    template_name = "registration/password_reset_form.html"


class PasswordResettingConfirmView(PasswordResetConfirmView):
    model = Redactor
    form_class = PasswordResettingFormConfirm
    success_url = reverse_lazy("agency_system:password-reset-success")
    template_name = "registration/password_reset_confirm.html"


class PasswordResetSuccess(TemplateView):
    template_name = "registration/password_reset_success.html"


class AddCommentView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "agency_system/comment_form.html"

    def get_success_url(self):
        return reverse_lazy("agency_system:newspaper-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.post_comment = Newspaper.objects.get(pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return_url"] = reverse_lazy("agency_system:newspaper-detail", kwargs={"pk": self.kwargs["pk"]})
        return context


class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    fields = ["body"]
    template_name = "agency_system/comment_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["return_url"] = reverse_lazy("agency_system:comment-and-replies", kwargs={"pk": self.kwargs["pk"]})
        return context

    def get_success_url(self):
        return reverse_lazy("agency_system:comment-and-replies", kwargs={"pk": self.kwargs["pk"]})


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = "agency_system/comment_confirm_delete.html"
    success_url = reverse_lazy("agency_system:newspaper-detail")

    def get_success_url(self):
        deleted_comment_id = self.kwargs["pk"]
        newspaper_id = Comment.objects.get(id=deleted_comment_id).post_comment.id
        return reverse_lazy("agency_system:newspaper-detail", kwargs={"pk": newspaper_id})


class ReplyCommentView(LoginRequiredMixin, generic.CreateView):
    model = ReplyComment
    form_class = ReplyCommentForm
    template_name = "agency_system/comment_reply_form.html"

    def get_success_url(self):
        return reverse_lazy("agency_system:newspaper-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_authors_username(self):
        comment_id = self.kwargs.get("comment_id")
        comment = Comment.objects.get(id=comment_id)
        return comment.author.username

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors_username"] = self.get_authors_username()
        context["news_list"] = Newspaper.objects.all()
        context["return_url"] = reverse_lazy("agency_system:newspaper-detail", kwargs={"pk": self.kwargs["pk"]})
        return context

    def form_valid(self, form):
        comment = Comment.objects.get(id=self.kwargs["comment_id"])
        form.instance.comment_author = comment
        form.instance.reply_author = self.request.user
        return super().form_valid(form)


class CommentAndRepliesView(LoginRequiredMixin, generic.DetailView):
    model = Comment
    template_name = "agency_system/comment_with_replies_detail.html"

    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        comment = Comment.objects.get(pk=comment_id)
        replies = comment.comment_replies.all()

        context = {
            "comment": comment,
            "replies": replies,
            "return_url": reverse_lazy("agency_system:newspaper-detail", kwargs={"pk": comment.post_comment.id})
        }

        return render(request, self.template_name, context)


class ReplyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ReplyComment
    fields = ["reply_body"]
    template_name = "agency_system/reply_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        updated_reply_id = self.kwargs["pk"]
        reply_comment = ReplyComment.objects.get(id=updated_reply_id)
        comment_id = reply_comment.comment_author.id
        context["return_url"] = reverse_lazy("agency_system:comment-and-replies", kwargs={"pk": comment_id})
        context["reply_author_id"] = reply_comment.reply_author.id if reply_comment.reply_author else None
        return context

    def get_success_url(self):
        updated_reply_id = self.kwargs["pk"]
        reply_comment = ReplyComment.objects.get(id=updated_reply_id)
        comment_id = reply_comment.comment_author.id
        return reverse_lazy("agency_system:comment-and-replies", kwargs={"pk": comment_id})


class ReplyDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ReplyComment
    template_name = "agency_system/reply_confirm_delete.html"

    def get_success_url(self):
        deleted_reply_id = self.kwargs["pk"]
        reply_comment = ReplyComment.objects.get(id=deleted_reply_id)
        comment_id = reply_comment.comment_author.id
        return reverse_lazy("agency_system:comment-and-replies", kwargs={"pk": comment_id})
