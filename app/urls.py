from django.urls import path

from app.views import AllPersonView

urlpatterns = [
    path('person/', AllPersonView.as_view(), name='person-list'),
]
