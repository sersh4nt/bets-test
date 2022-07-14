from .views import post_event
from django.urls import path

urlpatterns = [
    path("post-event/", post_event),
]
