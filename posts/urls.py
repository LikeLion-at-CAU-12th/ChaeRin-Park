from django.urls import path
from posts.views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('page', index, name='my-page'),
    path('introduction', codeReviewer, name='codeReviewer'),
]