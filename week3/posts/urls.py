from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('introduction', codeReviewer, name = 'codeReviewer'),
    path('page', codeReviewChallenge, name='my-page'),
]