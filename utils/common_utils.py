from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError

def handle_404(req, **kwargs):

    return HttpResponseNotFound(
        render(req,'common/404.html')
    )


def handle_500(req, **kwargs):

    return HttpResponseServerError(
        render(req,'common/500.html')
    )

def get_nearby_pages(page=None, limit=5):
    if not page:
        return None
    last_page = page.number + limit
    if last_page > page.paginator.num_pages:
        last_page = page.paginator.num_pages
    first_page = page.number - limit
    if first_page < 1:
        first_page = 1
    return range(first_page,last_page + 1)