from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError

def handle_404(req):

    return HttpResponseNotFound(
        render(req,'common/404.html')
    )


def handle_500(req):

    return HttpResponseServerError(
        render(req,'common/500.html')
    )