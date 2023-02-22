from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from time import sleep
from .tasks import send_email_task
import requests as r
# Create your views here.
def send_email(request):
    send_email_task.delay()
    return HttpResponse('<h1>email sent successfully.</h1>')


from django.views.decorators.cache import cache_page
from django.core.cache import cache


def test2(request):
    res = cache.get('test_delay_api')
    if res == None:
        res = r.get('https://e43698cb-d56c-428a-a101-131a5b2deb62.mock.pstmn.io/test/delay/5/').json()
        cache.set('test_delay_api', res, 5*60)
    
    return JsonResponse(res)


@cache_page(60)
def test(request):
    res = r.get('https://e43698cb-d56c-428a-a101-131a5b2deb62.mock.pstmn.io/test/delay/5/').json()
    return JsonResponse(res)
