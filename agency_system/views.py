from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Topic, Redactor, Newspaper


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_topics = Topic.objects.count()
    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    context = {
        "num_topics": num_topics,
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers
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


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    fields = ("username", "first_name", "last_name", "years_of_experience",)
    success_url = reverse_lazy("agency_system:redactor-list")
    template_name = "agency_system/redactor_form.html"


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    fields = ("username", "first_name", "last_name", "years_of_experience",)
    success_url = reverse_lazy("agency_system:redactor-list")
    template_name = "agency_system/redactor_form.html"


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic")


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
    template_name = "agency_system/newspaper_form.html"
