from django.shortcuts import render
from django.http import HttpResponse


def mail_view(request):
    return HttpResponse("Mail system is working!")
