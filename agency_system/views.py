from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .forms import (RedactorCreationForm,
                    RedactorEditForm,
                    PasswordsChangingForm,
                    PasswordsResettingForm,
                    PasswordsResettingFormConfirm
                    )
from .models import Topic, Redactor, Newspaper, Comment


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


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic


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


class TopicDeleteView(LoginRequiredMixin, generic.DetailView):
    model = Topic
    template_name = "agency_system/topic_confirm_delete.html"
    success_url = reverse_lazy("agency_system:topic-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor


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

    def get_success_url(self):
        return reverse_lazy("agency_system:redactor-detail", kwargs={"pk": self.object.pk})


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("agency_system:newspaper-list")
    template_name = "agency_system/newspaper_form.html"


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("agency_system:newspaper-list")
    template_name = "agency_system/newspaper_update.html"


class RegistrationSuccessView(TemplateView):
    template_name = 'registration/registration_success.html'


class PasswordChangedSuccessView(TemplateView):
    template_name = "registration/password_changed_success.html"


class PasswordsChangingView(PasswordChangeView):
    model = Redactor
    form_class = PasswordsChangingForm
    success_url = reverse_lazy("agency_system:password-changed")
    template_name = "registration/password_change.html"


class PasswordsResettingView(PasswordResetView):
    model = Redactor
    form_class = PasswordsResettingForm
    success_url = reverse_lazy("agency_system:password-reset")
    template_name = "registration/password_reset_form.html"


class PasswordsResettingConfirmView(PasswordResetConfirmView):
    model = Redactor
    form_class = PasswordsResettingFormConfirm
    success_url = reverse_lazy("agency_system:password-reset-success")
    template_name = "registration/password_reset_confirm.html"


class PasswordResetSuccess(TemplateView):
    template_name = "registration/password_reset_success.html"
