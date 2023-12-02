from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Topic, Redactor,Newspaper



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
